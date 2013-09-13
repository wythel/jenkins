#!/bin/bash
# get package
python $WORKSPACE/scripts/fetch_splunk.py --branch=$OLD_BRANCH --pkg-dir=$WORKSPACE --splunk-dir=$WORKSPACE

# start splunk
$WORKSPACE/splunk/bin/splunk start --accept-license --answer-yes
