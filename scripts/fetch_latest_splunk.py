import urllib
from optparse import OptionParser
import os
import subprocess
from datetime import datetime

def print_time_spent(time, pkg):
    """
    print how much time spent and the avg internet speed
    """
    print "Finished downloading, it took {t} seconds".format(t=time)
    speed = (os.path.getsize(pkg) / 1024) / time
    print "Average speed: {s} kilobytes per second".format(s=speed)

def dluntar(url):
    """
    Dowload and then untar splunk package, calculate time spent also
    """
    TAR_DIR = "/home/eserv/branches_tar"
    RUN_DIR = "/home/eserv/splunk_run"
    # download the tgz file
    # find the brach name and build number

    branch = url.split("/")[4].replace("_builds", "")
    build = url.split("/")[-1].replace("splunk-", "").replace("-Darwin-universal.tgz","")
    file_name = url.split("/")[-1]

    path = os.path.join(TAR_DIR, branch)
    if not os.path.exists(path):
        os.mkdir(path)

    tar_file = os.path.join(TAR_DIR, branch, file_name)
    if not os.path.exists(tar_file):
        try:
            print "Dowloading: {u}".format(u=url)
            print "to: {f}".format(f=tar_file)
            start = datetime.now()
            urllib.urlretrieve(url, tar_file)
            end = datetime.now()
            diff = end - start
            print_time_spent(time=diff.seconds, pkg=tar_file)
        except IOError, err:
            print "Can not open url. Did you connect to Splunk VPN?"
            print "ERROR: " + err
            exit(1)

    # untar the file
    branch_path = os.path.join(RUN_DIR, branch)
    if not os.path.exists(branch_path):
        os.mkdir(branch_path)
    untar_path = os.path.join(RUN_DIR, branch, build)
    if not os.path.exists(untar_path):
        os.mkdir(untar_path)
    command = "tar xf {tar} -C {path}".format(tar=tar_file, path=untar_path)
    print "Running '{c}'".format(c=command)
    p = subprocess.Popen(command, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    print os.path.join(untar_path, "splunk", "bin")

def main():
    # parse options
    parser = OptionParser()
    parser.add_option("-b", "--branch", dest="branch", help="brach to fetch")
    parser.add_option("-c", "--p4change", dest="cl", help="change list number to fetch")
    (options, args) = parser.parse_args()

    branch = options.branch
    cl = options.cl

    url_template = ("http://releases.splunk.com/cgi-bin/splunk_build_fetcher.py"
                    "?PLAT_PKG=Darwin-universal.tgz&DELIVER_AS=url&BRANCH={b}")
    if cl is not None:
        url_template = url_template + "&P4CHANGE={c}".format(c=cl)

    # get url of latest package
    f = urllib.urlopen(url_template.format(b=branch))
    pkg_url = f.readline().strip()

    if "Error" in pkg_url:
        print pkg_url
        exit(1)
    else:
        # run dluntar
        dluntar(pkg_url)

if __name__ == '__main__':
    main()

