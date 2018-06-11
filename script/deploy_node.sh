#!/bin/bash

SOURCE_URL=$1
DP_DIR=$2
TARGET_DIR=$3
SERVICE=`echo $TARGET_DIR | awk -F'[/]' '{print $NF}'`

PACKAGE=`basename $SOURCE_URL`
IP=`ifconfig | grep -A 1 bond0 | grep inet | awk -F'[:]' '{print $2}' | awk -F'[ ]' '{print $1}'|head -n 1`


function deploy()
{
mkdir -p ${DP_DIR}
if [ $? -ne 0 ]; then
	echo "Make deploy dir ${DP_DIR} failed."
	exit 1
fi


cd ${DP_DIR}

wget -c ${SOURCE_URL} -O $PACKAGE
if [ $? -ne 0 ]; then
	echo "Get package ${SOURCE_URL} failed."
	exit 1
fi


tar xzf $PACKAGE
if [ $? -ne 0 ]; then
	echo "Untar package ${PACKAGE} failed."
	exit 1
fi
# clean tarball
rm $PACKAGE

# change owner to www-data
chown www-data:www-data -R ${DP_DIR}

if [ -d $TARGET_DIR ]; then
	mv -f $TARGET_DIR ${TARGET_DIR}_`date +'%s'`

	if [ $? -ne 0 ]; then
		echo "Backup target dir ${TARGET_DIR} failed."
		exit 1
	fi
fi

if [ ! -f ${TARGET_DIR} ]; then
	cd ${TARGET_DIR}
	pm2 stop all
fi

mkdir -p ${TARGET_DIR}
chown www-data:www-data ${TARGET_DIR}
mv ${DP_DIR}/* ${TARGET_DIR}
if [ $? -ne 0 ]; then
	echo "Deploy target dir ${TARGET_DIR} failed."
	exit 1
fi

cd ${TARGET_DIR}
pm2 start app.js -i max

echo "Deploy ${TARGET_DIR} successfully."
}

function restart_docker()
{
/usr/bin/docker restart `/usr/bin/docker ps -a | grep $SERVICE | awk '{print $1}'`
}

case $IP in
    172.19.0.11)
        deploy
        restart_docker
        ;;
    *)
        deploy;;
esac
