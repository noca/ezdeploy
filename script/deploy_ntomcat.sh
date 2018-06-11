#!/bin/bash

source /etc/profile

SOURCE_URL=$1
DP_DIR=$2
TARGET_DIR=$3
PACKAGE=`basename $SOURCE_URL | awk -F"_" '{print $1}'`
WORKING_DIR=`echo $PACKAGE | awk -F"." '{print $1}'`
PORT=`xmlstarlet sel -t -m "/Server/Service/Connector" -v "@port" ${TARGET_DIR}/conf/server.xml`

if [ "$PORT" == "" ]; then
    echo "Wrong port.\n"
    exit 1
fi

#STOP_SCRIPT="ps -ef | grep java | grep ${TARGET_DIR} | grep -v 'grep' | awk '{print \$2}' | xargs kill -9"
STOP_SCRIPT="supervisorctl stop ${WORKING_DIR} &>/dev/null"
STATUS_SCRIPT="curl -i http://127.0.0.1:${PORT}/${WORKING_DIR} >/dev/null 2>&1"

# may be ansible will send sighup after it finish script, so nohup
START_SCRIPT="supervisorctl start ${WORKING_DIR} &>/dev/null"
#START_SCRIPT="nohup ./tomcat.sh start >/dev/null 2>&1"

mkdir -p ${DP_DIR}
if [ $? -ne 0 ]; then
	echo "Make deploy dir ${DP_DIR} failed. \n"
	exit 2
fi

rm ${DP_DIR}/${PACKAGE}

wget ${SOURCE_URL} -O ${DP_DIR}/${PACKAGE}
if [ $? -ne 0 ]; then
	echo "Get package ${SOURCE_URL} failed. \n"
	exit 3
fi

zipinfo ${DP_DIR}/${PACKAGE}
if [ $? -ne 0 ]; then
	echo "package ${PACKAGE} not a valid war package.\n"
	exit 8
fi

`eval ${STOP_SCRIPT}`
if [ $? -ne 0 ]; then
    echo "Stop failed.\n"
    exit 4
fi
sleep 1

`eval ${STATUS_SCRIPT}`
if [ $? -eq 0 ]; then
    echo "Stop failed.\n"
    exit 5
fi

if [ "$PACKAGE" != "" ]; then
    rm -rf "${TARGET_DIR}/webapps/${PACKAGE}"
    rm -rf "${TARGET_DIR}/webapps/${WORKING_DIR}"
fi

mkdir -p ${TARGET_DIR}/webapps/
mv ${DP_DIR}/${PACKAGE} ${TARGET_DIR}/webapps/${PACKAGE}
if [ $? -ne 0 ]; then
	echo "Deploy target dir ${TARGET_DIR} failed.\n"
	exit 8
fi

cd ${TARGET_DIR}
`eval ${START_SCRIPT}`
if [ $? -ne 0 ]; then
    echo "Start failed."
    exit 6
fi

echo "Starting...\n"
counter=0
while [ $counter -lt 10 ]; do
    `eval ${STATUS_SCRIPT}`
    if [ $? -eq 0 ]; then
	    break
    fi
    let counter=counter+1
    echo "$counter"
    sleep 1
done

if [ $counter -ge 10 ]; then
    echo "Deploy failed.\n"
    exit 7
fi

echo "Deploy ${TARGET_DIR} successfully."
exit 0
