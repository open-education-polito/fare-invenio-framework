#!/bin/bash

echo "Saving all the metadata..."
docker exec fare-invenio_db_1 pg_dumpall -U fare > ~/fare_shared_data/fare_db/backup_fare_db.sql

# checking if repo already exists or not
REPO=$(curl -X GET "localhost:9200/_cat/repositories" | wc -l)
echo "Number of repos: $REPO"

if [ $REPO -eq 0 ]
then
  echo "Creating the repo..."
  curl -X PUT -H "Content-Type: application/json" -d '{ "type": "fs", "settings": { "compress": true, "location": "." } }' http://localhost:9200/_snapshot/backup_fare_es
  echo
else
  echo "Repo exists..."
fi

# checking number of snapshot to create the new snapshot with the correct name 'snapshot_<#number>'
echo "Checking number of snapshots..."
SNAPSHOTS=$(curl -X GET "localhost:9200/_cat/snapshots/backup_fare_es" | wc -l)
echo "Number of snapshots: $SNAPSHOTS"
echo "Next snapshot's name: snapshot_$(($SNAPSHOTS+1))"
echo "Saving all the indexes..."
curl -X PUT http://localhost:9200/_snapshot/backup_fare_es/snapshot_$(($SNAPSHOTS+1))?wait_for_completion=true
echo
