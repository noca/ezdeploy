#!/bin/bash

source /etc/profile

PK_DIR=$1
PG_DIR=$2

MAIN_DIR="`basename $PK_DIR`-main"

cd ${PK_DIR}
mvn clean install -am -Dmaven.test.skip >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Package ${PK_DIR} failed"
    exit 1
fi

pnum=`find ${PK_DIR}  -name "*.zip"|grep -i "${MAIN_DIR}/target/" | wc -l`
if [ $pnum -ne 1 ]; then
    echo "${PK_DIR}/${MAIN_DIR} target not uniq"
    exit 1
fi

TARGET=`find ${PK_DIR}  -name "*.zip"|grep -i "${MAIN_DIR}/target/"`


tar czfP  ${TARGET}.tar.gz  -C `echo $TARGET|awk -F 'target/' '{print $1"target"}'` `echo $TARGET|awk -F 'target/' '{print $2}'`

echo -n "${TARGET}.tar.gz"
