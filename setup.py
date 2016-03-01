import sys
from setuptools import setup

VERSION = "16.01.01"
def build():
    setup(
        name="DivvyCloud Process Health"
        ,version=VERSION
        ,description="Provides API endpoints for retrieving DivvyCloud process health information"
        ,author='Divvy Corp.'
        ,author_email='developers@divvycloud.com'
        ,platforms=['any']
        ,license='(c)2016 Divvy Corp.'
        ,keywords = "divvycloud plugins health"
        ,zip_safe = False
        ,url = "https://www.divvycloud.com"
        ,packages = ["divvy-process-health"]
        ,package_dir={"divvy-process-health" : "cooked/divvycloud_process_health"}
        ,package_data = {"divvy-process-health" : [
                                                'plugin.json']
                                            }
        ,entry_points = {"divvycloud.plugins" : 'plugin_entry = plugin:load'}
        ,classifiers = [
            "Development Status :: 4 - Beta",
            "Topic :: Utilities"
        ]
    )

if __name__ == "__main__":
    if "--override-version" in sys.argv:
        try:
            idx = sys.argv.index("--override-version")
            VERSION = sys.argv[idx+1]
            del sys.argv[idx+1]
            del sys.argv[idx]
        except:
            print "--override-version was used without a version"
            print "Usage Eg: python setup.py --override-version 11.11.11"

    build()

