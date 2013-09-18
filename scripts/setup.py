import os, sys
import subprocess
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

def download_pkg():
    print "Downloading pkg..."
    # download and untar package
    workspace = os.environ['WORKSPACE']
    old_branch = os.environ['OLD_BRANCH']

    cmd = ("python {w}/scripts/fetch_splunk.py --branch={b} "
           "--pkg-dir={w} --splunk-dir={w}".format(w=workspace, b=old_branch))

    if "OLD_BUILD" in os.environ:
        cmd = cmd + " --p4change={build}".format(build=os.environ["OLD_BUILD"])

    # call the command
    print cmd
    p = subprocess.Popen(cmd, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    print "complete"

def start_splunk():
    print "Starting splunk..."
    cmd = "$WORKSPACE/splunk/bin/splunk start --accept-license --answer-yes"
    if "OLD_BUILD" in os.environ:
        cmd = cmd + " --p4change=$OLD_BUILD"

    # call the command
    p = subprocess.Popen(cmd, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()

def start_firefox():
    print "Starting firefox"
    os.environ["DISPLAY"] = ":0.0"
    a = Firefox()
    a.get("http://www.google.com")
    print a.title
    a.close()

def main():
    download_pkg()
    start_splunk()
    start_firefox()

if __name__ == '__main__':
    main()