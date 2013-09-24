import os, sys
import subprocess
from optparse import OptionParser

def execute_command(cmd):
    """
    execute a shell command
    """
    # call the command
    p = subprocess.Popen(cmd, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    return p

def download_pkg(branch, build=None):
    print "Downloading pkg..."
    # download and untar package
    workspace = os.environ['WORKSPACE']

    cmd = ("python {w}/scripts/fetch_splunk.py --branch={b} "
           "--pkg-dir={w} --splunk-dir={w}".format(w=workspace, b=branch))

    if build is not None:
        cmd = cmd + " --p4change={build}".format(build=build)

def start_splunk():
    print "Starting splunk..."
    cmd = "$WORKSPACE/splunk/bin/splunk start --accept-license --answer-yes"
    execute_command(cmd)

def stop_splunk():
    print "Stoping splunk"
    cmd = "$WORKSPACE/splunk/bin/splunk stop"
    execute_command(cmd)

def parse_options():
    """
    parse options
    """
    parser = OptionParser()
    parser.add_option("--migration", dest="migration", action="store_true",
                      help="if this flag is set, we run migration"
                           ", else we start a new splunk")
    (options, args) = parser.parse_args()
    return options

def main():
    options = parse_options()

    if options.migration:
        # do migration
        stop_splunk()
        build = os.environ['NEW_BUILD'] if 'NEW_BUILD' in os.environ else None
        download_pkg(branch=os.environ['NEW_BRANCH'], build=build)
        start_splunk()
    else:
        # start a new splunk
        build = os.environ['OLD_BUILD'] if 'OLD_BUILD' in os.environ else None
        download_pkg(branch=os.environ['OLD_BRANCH'], build=build)
        start_splunk()

if __name__ == '__main__':
    main()