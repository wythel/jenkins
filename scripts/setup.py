import os
import subprocess
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

def download_pkg():
    print "Downloading pkg..."
    # download and untar package
    cmd = ("python $WORKSPACE/scripts/fetch_splunk.py --branch=$OLD_BRANCH"
           " --pkg-dir=$WORKSPACE --splunk-dir=$WORKSPACE")

    if "OLD_BUILD" in os.environ:
        cmd = cmd + " --p4change=$OLD_BUILD"

    # call the command
    p = subprocess.Popen(cmd, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()

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
    a = Firefox()
    a.get("http://www.google.com")
    print a.title

def main():
    download_pkg()
    start_splunk()
    start_firefox()

if __name__ == '__main__':
    main()