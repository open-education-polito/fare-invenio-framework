#!/bin/bash

if [ -d "../fare_shared_data" ]
then
  echo "~/fare_shared_data already exists"
else
  mkdir ~/fare_shared_data
fi

if [ -d "../fare_shared_data/fare_db" ]
then
  echo "~/fare_shared_data/fare_db already exists"
else
  mkdir ~/fare_shared_data/fare_db
fi

if [ -d "../fare_shared_data/fare_es" ]
then
  echo "~/fare_shared_data/fare_es already exists"
else
  mkdir ~/fare_shared_data/fare_es
fi

if [ -d "../fare_shared_data/fare_files" ]
then
  echo "~/fare_shared_data/fare_files already exists"
else
  mkdir ~/fare_shared_data/fare_files
fi

echo "Saving all the metadata in the host at ~/fare_shared_data/fare_db..."
docker exec fare-invenio_db_1 pg_dumpall -U $PG_USER > ~/fare_shared_data/fare_db/backup_fare_db.sql

# checking if repo already exists or not
REPO=$(docker exec fare-invenio_es_1 curl -s -X GET "localhost:9200/_cat/repositories" | wc -l)

if [ $REPO -eq 0 ]
then
  echo "Creating the repo..."
  docker exec fare-invenio_es_1 curl -s -X PUT -H "Content-Type: application/json" -d '{ "type": "fs", "settings": { "compress": true, "location": "." } }' http://localhost:9200/_snapshot/backup_fare_es
  echo
else
  echo "Repo exists..."
fi

# checking number of snapshot to create the new snapshot with the correct name 'snapshot_<#number>'
echo "Checking number of snapshots..."
SNAPSHOTS=$(docker exec fare-invenio_es_1 curl -s -X GET "localhost:9200/_cat/snapshots/backup_fare_es" | wc -l)
echo "Number of snapshots: $SNAPSHOTS"
echo "Saving all the indexes..."
docker exec fare-invenio_es_1 curl -s -X PUT http://localhost:9200/_snapshot/backup_fare_es/snapshot_$(($SNAPSHOTS+1))?wait_for_completion=true > /dev/null 2>&1

# saving elasticsearch dump in the host
echo "Saving Elasticsearch data in the host at ~/fare_shared_data/fare_es..."
docker cp fare-invenio_es_1:/usr/share/elasticsearch/backup_fare_es/. ~/fare_shared_data/fare_es/

# saving files in the host
echo "Saving files in the host at ~/fare_shared_data/fare_files..."
docker cp fare-invenio_web-ui_1:/opt/invenio/var/instance/data/. ~/fare_shared_data/fare_files/
