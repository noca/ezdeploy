#!/bin/bash

PK_DIR=$1
PG_DIR=$2

NAME=`basename $PK_DIR`
TARGET=${PG_DIR}/${NAME}.tar.gz

if [ -d "${PK_DIR}/public" ];then
    touch ${PK_DIR}/public/health
    touch ${PK_DIR}/health
else
    touch ${PK_DIR}/health
fi

tar czf ${TARGET} -C ${PK_DIR} `ls ${PK_DIR}`

echo -n "${TARGET}"
