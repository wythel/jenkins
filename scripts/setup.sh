#!/bin/bash
python $WORKSPACE/scripts/fetch_splunk.py --branch=$BRANCH --pkg-dir=$WORKSPACE --splunk-dir=$WORKSPACE
$WORKSPACE/splunk/bin/splunk start --accept-license --answer-yes
