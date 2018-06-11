#!/bin/bash

PK_DIR=$1
PG_DIR=$2

NAME=`basename $PK_DIR`
TARGET=${PG_DIR}/${NAME}.tar.gz

tar czf ${TARGET} -C ${PK_DIR} `ls ${PK_DIR}`

echo -n "${TARGET}"
