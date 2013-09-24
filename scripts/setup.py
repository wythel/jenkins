import os, sys
import subprocess
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

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
    if "OLD_BUILD" in os.environ:
        cmd = cmd + " --p4change=$OLD_BUILD"
    execute_command(cmd)

def main():
    build = os.environ['OLD_BUILD'] if 'OLD_BUILD' in os.environ else None
    download_pkg(branch=os.environ['OLD_BRANCH'], build=build)
    start_splunk()

if __name__ == '__main__':
    main()