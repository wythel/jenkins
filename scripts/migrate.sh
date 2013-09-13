# stop splunk
$WORKSPACE/splunk/bin/splunk stop

#migrate
python $WORKSPACE/scripts/fetch_splunk.py --branch=$OLD_BRANCH --pkg-dir=$WORKSPACE --splunk-dir=$WORKSPACE

# start splunk
$WORKSPACE/splunk/bin/splunk start --accept-license --answer-yes