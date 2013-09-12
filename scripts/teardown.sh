#!/bin/bash
echo "Tearing down splunk..."
rm $WORKSPACE/*.tgz
rm -rf $WORKSPACE/splunk
