#!/bin/bash
echo "Tearing down splunk..."
$WORKSPACE/splunk/bin/splunk stop
rm $WORKSPACE/*.tgz
rm -rf $WORKSPACE/splunk
ls -lh $WORKSPACE
