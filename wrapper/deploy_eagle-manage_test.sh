#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <package url>"
    exit 1
fi



PACKAGE_URL=$1

SERVICE="eagle-manage"
name=`basename $1|awk -F '.' '{print $1}'`
if [ "$SERVICE" == "$name" ]
 then
    echo -e "name ok"
 else
    echo -e "name no"
    exit 9
fi

ENV="test"
WR="/data/www/auth_api"
DS="../script/deploy_php.sh"

cd ../mcdeploy/

/usr/bin/python run.py -s ${SERVICE} deploy \
		-p ${PACKAGE_URL} \
		-de ${ENV} \
		-wr ${WR} \
		-ds ${DS}
