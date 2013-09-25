import urllib
from optparse import OptionParser
import os
import subprocess
from datetime import datetime
import logging

def print_time_spent(time, pkg):
    """
    print how much time spent and the avg internet speed
    """
    logger.info("Finished downloading, it took {t} seconds".format(t=time))
    speed = (os.path.getsize(pkg) / 1024) / time
    logger.info("Average speed: {s} kilobytes per second".format(s=speed))

def dluntar(url, tar_dir, run_dir):
    """
    Dowload and then untar splunk package, calculate time spent also
    """
    TAR_DIR = tar_dir #"/Users/clin/branches_tar"
    RUN_DIR = run_dir #"/Users/clin/splunk_run"
    # download the tgz file
    # find the brach name and build number

    branch = url.split("/")[4].replace("_builds", "")
    build = url.split("/")[-1].replace("splunk-", "").replace("-Linux-x86_64.tgz","")
    file_name = url.split("/")[-1]

    tar_file = os.path.join(TAR_DIR, file_name)
    if not os.path.exists(tar_file):
        try:
            logger.info("Dowloading: {u}".format(u=url))
            logger.info("to: {f}".format(f=tar_file))
            start = datetime.now()
            urllib.urlretrieve(url, tar_file)
            end = datetime.now()
            diff = end - start
            print_time_spent(time=diff.seconds, pkg=tar_file)
        except IOError, err:
            logger.error("Can not open url. Did you connect to Splunk VPN?")
            logger,error("ERROR: " + err)
            exit(1)

    # untar the file
    command = "tar xf {tar} -C {path}".format(tar=tar_file, path=RUN_DIR)
    logger.info("Running '{c}'".format(c=command))
    p = subprocess.Popen(command, env=os.environ, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()

def parse_options():
    """
    parse options
    """
    parser = OptionParser()
    parser.add_option("-b", "--branch", dest="branch", help="brach to fetch")
    parser.add_option("-c", "--p4change", dest="cl", help="change list number to fetch")
    parser.add_option("-p", "--pkg-dir", dest="pkg_dir",
                      default="/Users/clin/branches_tar",
                      help="directory for saving the pkg, will mkdir if it does not exist")
    parser.add_option("-s", "--splunk-dir", dest="splunk_dir",
                      default="/Users/clin/splunk_run",
                      help="directory for untaring splunk, will mkdir if it does not exist")
    (options, args) = parser.parse_args()
    return options

def set_logger():
    # create logger
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    fh = logging.FileHandler("fetch_splunk.log", mode='a')
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(fh)
    return logger

def main():
    options = parse_options()
    branch = options.branch
    cl = options.cl
    pkg_dir = options.pkg_dir
    splunk_dir = options.splunk_dir

    global logger
    logger = set_logger()

    # check if pkg_dir and splunk_dir exist. if not, create them
    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)

    if not os.path.exists(splunk_dir):
        os.makedirs(splunk_dir)

    if branch is None:
        logger.error("Branch must be given, please use "
                     "'-b' option to specify a branch")
        exit(1)

    # getting the pkg url
    url_template = ("http://releases.splunk.com/cgi-bin/splunk_build_fetcher.py"
                    "?PLAT_PKG=Linux-x86_64.tgz&DELIVER_AS=url&BRANCH={b}")
    if cl is not None:
        logger.info("Getting splunk on branch '{b}' @ {cl}".format(b=branch,
                                                                   cl=cl))
        url_template = url_template + "&P4CHANGE={c}".format(c=cl)
    else:
        logger.info("Getting the latest splunk pkg on branch '{b}'"
                    .format(b=branch))

    # get url of latest package
    try:
        f = urllib.urlopen(url_template.format(b=branch))
        pkg_url = f.readline().strip()

        if "Error" in pkg_url:
            logger.error(pkg_url)
            exit(1)
        elif "" == pkg_url:
            logger.error("The pkg url is an empty string, "
                   "please check your parameters are correct")
            logger.error("Brach: {b}, build: {c}".format(b=branch, c=cl))
            exit(1)
        else:
            # run dluntar
            dluntar(url=pkg_url, tar_dir=pkg_dir, run_dir=splunk_dir)
    except IOError, err:
        logger.error(url_template.format(b=branch))
        logger.error(err)
        exit(1)

if __name__ == '__main__':
    main()
