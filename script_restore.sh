#!/bin/bash

echo "Restoring all the metadata..."
docker exec fare-invenio_db_1 psql -f /backup_fare_db/backup_fare_db.sql -U fare > /dev/null 2>&1

# checking if repo already exists or not
REPO=$(curl -X GET "localhost:9200/_cat/repositories" | wc -l)
echo "Number of repos: $REPO"

if [ $REPO -eq 0 ]
then
  echo "Recreating the repo..."
  curl -X PUT -H "Content-Type: application/json" -d '{ "type": "fs", "settings": { "compress": true, "location": "." } }' http://localhost:9200/_snapshot/backup_fare_es
  echo
else
  echo "Repo exists..."
fi


echo "Closing .kibana index..."
curl -X POST http://localhost:9200/.kibana/_close
echo

# checking number of snapshot to restore the correct snapshot with the name 'snapshot_<#number>'
echo "Checking number of snapshots..."
SNAPSHOTS=$(curl -X GET "localhost:9200/_cat/snapshots/backup_fare_es" | wc -l)
echo "Number of snapshots: $SNAPSHOTS"
echo "Restoring all the indexes..."
curl -X POST http://localhost:9200/_snapshot/backup_fare_es/snapshot_$SNAPSHOTS/_restore
echo

echo "Removing unused indexes..."
INDEXES=$(curl 'http://localhost:9200/_aliases?pretty=true' | grep -o 'records\-record\-v1.0.0\-[0-9]*')

FIRST=true
NUMB_INDEXES=0

for i in $INDEXES
do
  NUMB_INDEXES=$((NUMB_INDEXES+1))
done

echo "THERE ARE $NUMB_INDEXES INDEXES"

if [ $NUMB_INDEXES -gt 1 ]
then

  for i in $INDEXES
  do
    if [ $FIRST ]
    then
      FIRST=false
      OLDEST=$i
    else
      if [ $i < $OLDEST ]
      then
        OLDEST=$i
      fi
    fi
  done

  echo "OLDEST: $OLDEST"

  for i in $INDEXES
  do
    if [ $i != $OLDEST ]
    then
      curl -X DELETE "localhost:9200/$i?pretty" > /dev/null 2>&1
    fi
  done

fi
