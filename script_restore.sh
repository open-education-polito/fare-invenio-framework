#!/bin/bash

# copy dump of database metadata in the container
echo "Copying metadata in fare-invenio_db_1 container..."
docker cp ~/fare_shared_data/fare_db/backup_fare_db.sql fare-invenio_db_1:/backup_fare_db/

# copy elasticsearch dump in the container
echo "Copying Elasticsearch data in fare-invenio_es_1 container..."
docker cp ~/fare_shared_data/fare_es/. fare-invenio_es_1:/usr/share/elasticsearch/backup_fare_es/

# copy files dump in the container
echo "Copying files fare-invenio_web-ui_1 container..."
docker cp ~/fare_shared_data/fare_files/. fare-invenio_web-ui_1:/opt/invenio/var/instance/data/

echo "Restoring all the metadata..."
docker exec fare-invenio_db_1 psql -f /backup_fare_db/backup_fare_db.sql -U $PG_USER > /dev/null 2>&1

# checking if repo already exists or not
REPO=$(docker exec fare-invenio_es_1 curl -s -X GET "localhost:9200/_cat/repositories" | wc -l)

if [ $REPO -eq 0 ]
then
  echo "Recreating the repo..."
  docker exec fare-invenio_es_1 curl -s -X PUT -H "Content-Type: application/json" -d '{ "type": "fs", "settings": { "compress": true, "location": "." } }' http://localhost:9200/_snapshot/backup_fare_es
  echo
else
  echo "Repo exists..."
fi

echo "Check .kibana idex..."
TEMP=$(docker exec fare-invenio_es_1 curl -s -I "localhost:9200/.kibana?pretty" | grep -o 'OK')

if [[ $TEMP = "OK" ]]
then
  echo "Closing .kibana index..."
  docker exec fare-invenio_es_1 curl -s -X POST http://localhost:9200/.kibana/_close > /dev/null 2>&1
else
  echo ".kibana does not exists..."
fi

# checking number of snapshot to restore the correct snapshot with the name 'snapshot_<#number>'
echo "Checking number of snapshots..."
SNAPSHOTS=$(docker exec fare-invenio_es_1 curl -s -X GET "localhost:9200/_cat/snapshots/backup_fare_es" | wc -l)
echo "Number of snapshots: $SNAPSHOTS"
echo "Restoring all the indexes..."
docker exec fare-invenio_es_1 curl -s -X POST http://localhost:9200/_snapshot/backup_fare_es/snapshot_$SNAPSHOTS/_restore > /dev/null 2>&1

echo "Removing unused indexes..."

# creating the vector of indexes
INDEXES=($(docker exec fare-invenio_es_1 curl -s 'http://localhost:9200/_aliases?pretty=true' | grep -o 'records\-record\-v1.0.0\-[0-9]*'))

NUMB_INDEXES=${#INDEXES[@]}

if [ $NUMB_INDEXES -gt 1 ]
then

  # set first position of the array as the oldest and then compare all the element
  OLDEST=${INDEXES[0]}

  for i in ${INDEXES[@]}
  do
    if [[ $i < $OLDEST ]]
    then
      OLDEST=$i
    fi
  done

  for i in ${INDEXES[@]}
  do
    if [[ $i != $OLDEST ]]
    then
      echo "Removing index: $i"
      # docker exec fare-invenio_es_1 curl -s -X DELETE "localhost:9200/$i?pretty" > /dev/null 2>&1
    fi
  done

fi
