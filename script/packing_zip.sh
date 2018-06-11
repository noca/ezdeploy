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

pnum=`ls ${MAIN_DIR}/target/*.zip|grep -v original | wc -l`
if [ $pnum -ne 1 ]; then
    echo "${PK_DIR}/${MAIN_DIR} target not uniq"
    exit 1
fi

TARGET=`ls ${PK_DIR}/${MAIN_DIR}/target/*.zip`


tar czf ${TARGET}.tar.gz -C ${PK_DIR}/${MAIN_DIR}/target `ls ${PK_DIR}/${MAIN_DIR}/target/*.zip|xargs basename`

echo -n "${TARGET}.tar.gz"
