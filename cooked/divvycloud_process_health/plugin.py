from DivvyBlueprints.v2 import Blueprint
from DivvyPlugins.plugin_helpers import register_api_blueprint, unregister_api_blueprints
from DivvySession import DivvySession
from DivvyBlueprints import get_ondemand_queue
from DivvyUtils.flask_helpers import JsonResponse
from DivvyPlugins.plugin_metadata import PluginMetadata
from collections import defaultdict
from DivvyRQ.DivvyRQ import DivvyRQProxyWorker



class metadata(PluginMetadata):
    version = '1.0'
    last_updated_date = '2016-02-29'
    author = 'Divvy Cloud Corp.'
    nickname = 'DivvyCloud Process Health'
    default_language_description = 'DivvyCloud Process Health plugin allows users to retrieve process by process health'
    support_email = 'support@divvycloud.com'
    support_url = 'http://support.divvycloud.com'
    main_url = 'http://www.divvycloud.com'
    managed = True
    divvy_api_version = "16.01"


blueprint = Blueprint('status', __name__, static_folder='html', template_folder='html')
@blueprint.routeUnauthenticated('/get_status', methods=['POST','GET'])
def get_queues_status():
    """
    Retrieve a list of DivvyCloud processes
    """
    process_list = []

    # Retrieve redis connection data from our ondemand queue
    redis_queue = get_ondemand_queue().redis_queue
    connection = redis_queue.connection

    workers_by_queue = defaultdict(set)
    for worker in DivvyRQProxyWorker.all(connection=connection):
        for queue_name in worker.queue_names():
            workers_by_queue[worker.name].add(queue_name)

    # Get a list of divvy cloud processes
    processes = connection.keys('divvy.process.*')

    for process in processes:
        time_stamp = connection.get(process)
        proc_type = process.split(":")[0].split(".")[2]
        host = process.split(":")[1]
        pid = process.split(":")[2]
        ttl = connection.ttl(process)
        shortname, _, _ = host.partition(".")
        full_proc_name = "%s.%s" % (shortname,pid)
        process_list.append({
            "process_type" :  proc_type
            ,"host" : host
            ,"last_checkin_time" :  time_stamp
            ,"PID" : pid
            ,"TTL" : ttl
            ,"queues" : list(workers_by_queue[full_proc_name])
        })

    return JsonResponse({'process_list' : process_list})


def load():
    register_api_blueprint(blueprint)


def unload():
    unregister_api_blueprints()


