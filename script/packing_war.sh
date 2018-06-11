#!/bin/bash

source /etc/profile

PK_DIR=$1
PG_DIR=$2

cd ${PK_DIR}
mvn clean package -am -Dmaven.test.skip >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Package ${PK_DIR} failed"
    exit 1
fi

pnum=`ls target/*.war | wc -l`
if [ $pnum -ne 1 ]; then
    echo "${PK_DIR} target not uniq"
    exit 1
fi

TARGET=`ls ${PK_DIR}/target/*.war`
echo -n "${TARGET}"
