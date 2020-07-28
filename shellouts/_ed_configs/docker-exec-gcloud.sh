#!/bin/bash

export GCLOUD_CONTAINER_CMD=${GCLOUD_CONTAINER_CMD:=gcloud projects list}
export GCLOUD_CONTAINER_NAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)

docker pull google/cloud-sdk:latest 2>&1 > /dev/null

#echo ""
#docker run -ti google/cloud-sdk:latest gcloud version
#echo ""
#docker rm -fv $GCLOUD_CONTAINER_NAME 2>&1 > /dev/null

for i in `docker ps -a|grep gcloud| cut -d " " -f 1`; do echo $i; docker rm -fv $i; done

echo ""
echo "Executing CMD $GCLOUD_CONTAINER_CMD in container_name $GCLOUD_CONTAINER_NAME"

docker run -ti -v $GOOGLE_APPLICATION_CREDENTIALS:$GOOGLE_APPLICATION_CREDENTIALS --name $GCLOUD_CONTAINER_NAME google/cloud-sdk gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS 2>&1 > /dev/null || exit 9
echo ""

echo "_ed_output"
docker run --rm -ti --volumes-from $GCLOUD_CONTAINER_NAME google/cloud-sdk $GCLOUD_CONTAINER_CMD || exit 9
echo "_ed_output"
echo ""

for i in `docker ps -a|grep gcloud| cut -d " " -f 1`; do docker rm -fv $i 2>1 > /dev/null; done
#docker rm -fv $GCLOUD_CONTAINER_NAME 2>&1 > /dev/null
