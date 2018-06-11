#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <branch>"
    exit 1
fi

GIT_BRANCH=$1

SERVICE="eagle-manage"

GIT_REPO="http://ccegitlab.creditease.corp/devops/eagle.git"
CONF_REPO="http://ccegitlab.creditease.corp/library/service-conf.git"
CONF_BRANCH="master"
CONF_SERVICE="eagle-manage"
ENV="test"
BS="../script/packing_python.sh"

cd ../ezdeploy/

python run.py -s ${SERVICE} pack \
		-r ${GIT_REPO} \
		-b ${GIT_BRANCH} \
		-cr ${CONF_REPO} \
		-cb ${CONF_BRANCH} \
		-cs ${CONF_SERVICE} \
		-pe ${ENV} \
		-bs ${BS}
