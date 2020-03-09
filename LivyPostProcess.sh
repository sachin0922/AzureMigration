#!/bin/bash

#0 - Success
#1 - Dead
#2 - Job Not submitted

dt=`date +%Y%m%d_%H%M%S`
logFile=/home/datalake/post-pro/LogPostProess-$dt.log
echo "Starting with Post Process at - $dt" >> $logFile

response=`curl -k --user "<user>:<pass>" -v -H "Content-Type: application/json" -X POST -d '{ "file":"wasbs://<container@storage_url>/SparkSimpleApp-1.0-SNAPSHOT.jar", "className":"com.microsoft.spark.example.WasbIOTest" }' "https://<hdinsight server url>/livy/batches" -H "X-Requested-By: <user>"` >> $logFile
id=`echo $response | cut -d ':' -f2 | cut -d ',' -f1`

if [[ $id = '' ]]; then
    echo "Job was not submitted to Spark Cluster due to some reason...Exiting" >> $logFile
    exit 2
fi

while true;do
    echo "Retrying status check at - `date +%Y%m%d_%H%M%S`" >> $logFile
    resp=`curl -k --user "<user>:<pass>"  https://<hdinsight server url>/livy/batches/$id/state`
    state=`echo $resp | cut -d ':' -f3 | cut -d '"' -f2`


    if [[ "$state" = "dead" ]]
    then
        echo "Post Process killed/Failed at - `date +%Y%m%d_%H%M%S`" >> $logFile
        exit 1
    elif [[ "$state" = "success" ]]
    then
        echo "Completed Post Process at - `date +%Y%m%d_%H%M%S`" >> $logFile
        exit 0
    else
        echo "Waiting...." >>$logFile
        sleep 2
    fi
done