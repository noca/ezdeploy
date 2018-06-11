#!/bin/bash

SOURCE_URL=$1
DP_DIR=$2
TARGET_DIR=$3
PACKAGE=`basename $SOURCE_URL`

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

# make runtime dir
mkdir -p protected/runtime

# change owner to www-data
chown www-data:www-data -R ${DP_DIR}

if [ -d $TARGET_DIR ]; then
	mv -f $TARGET_DIR ${TARGET_DIR}_`date +'%s'`

	if [ $? -ne 0 ]; then
		echo "Backup target dir ${TARGET_DIR} failed."
		exit 1
	fi
fi

mkdir -p ${TARGET_DIR}
chown www-data:www-data ${TARGET_DIR}
mv ${DP_DIR}/* ${TARGET_DIR}
if [ $? -ne 0 ]; then
	echo "Deploy target dir ${TARGET_DIR} failed."
	exit 1
fi

/etc/init.d/php5-fpm reload

echo "Deploy ${TARGET_DIR} successfully."
