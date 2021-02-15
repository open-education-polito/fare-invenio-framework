# Backup and restore FARE

The backup is composed of three parts:
- Databse where all the metadata and the users are stored
- Elasticsearch used to index the records and search them
- Files stored in the container web-ui

## Backup strategy

There are two ways to backup data on FARE:
- Copying the folder `$FARE_DATA_PATH/fare-data` where `$FARE_DATA_PATH` is the variable specified in the `.env`
- Following the procedure described below. The steps described are automated by the scripts `backup` and `restore` as mentioned later.

## 1. Database
The dump of the metadata and the users can be done with this command:
```
docker exec fare-invenio_db_1 pg_dumpall -U $PG_USER > $FARE_DUMP_PATH/fare_data_dump/fare_db/backup_fare_db.sql
```
Where:
- `fare-invenio_db_1` is the name of the container
- `pg_dumpall` the command of postgres to dump all the database
- `-U $PG_USER` the user specified in the `.env` file
- `$FARE_DUMP_PATH/fare_data_dump/fare_db/backup_fare_db.sql` the path where to save the dump, $FARE_DUMP_PATH is specified in the `.env` file

In this way we have the database dump both on the `fare-invenio_db_1` container, in the directory `/backup_fare_db`, and on the host, in the path `$FARE_DUMP_PATH/fare_data_dump/fare_db/`. 

To restore the data we have to run this command:
```
docker exec fare-invenio_db_1 psql -f /backup_fare_db/backup_fare_db.sql -U $PG_USER
```

Where:
- `fare-invenio_db_1` is the name of the container
- `psql` the command of postgres to restore the data
- `-f /backup_fare_db/backup_fare_db.sql` the file where there is the database backup
- `-U $PG_USER` the user

## 2. Elasticsearch
First of all the path where to store the dump must be specified in the config file, it was done modifing the config file of elasticsearch in  `/docker/elasticsearch/elasticsearch.yml` adding the path of the repo `path.repo: ["<path_where_to_store_the_dump>"]`, doing so there is no need to stop and restart the container.

Inside the container of elasticsearch the config file is in `config/elasticsearch.yml` , **could be necessary to change the permissions of the specified path**.

The curl request to create the repo where to store the snapshot is:
```
curl -X PUT -H "Content-Type: application/json" -d '{ "type": "fs", "settings": {
"compress": true, "location": "." } }'
http://localhost:9200/_snapshot/backup_fare
```

To make the dump you need to do the following request:
```
curl -X PUT http://localhost:9200/_snapshot/backup_fare/snapshot_1?
wait_for_completion=true
```

Now you have your backup, if you want to restore the data you need to follow this steps:
- `curl -X POST http://localhost:9200/_snapshot/backup_fare_es/snapshot_1/_restore`
- **There could be an error that says to close the .kibana index**, in that case do:
`curl -X POST http://localhost:9200/.kibana/_close`

If after the restore is not possible to create new files, probably is because there
are two indexes, so delete one of them, in particular you can see them with `curl
http://localhost:9200/_aliases?pretty=true` the output should be something like:
```
{
  "records-record-v1.0.0-1600787285" : {
    "aliases" : {
      "records" : { },
      "records-record-v1.0.0" : { }
    }
  },
  ".kibana_1" : {
    "aliases" : {
      ".kibana" : { }
    }
  },
  "records-record-v1.0.0-1601302875" : {
    "aliases" : {
      "records" : { },
      "records-record-v1.0.0" : { }
    }
  }
}

```

You can see there are two `records-record-v1.0.0-<timestamp>`, so all you need is to
delete the index with the most recent `<timestamp>` with:
- `curl -X DELETE "localhost:9200/records-record-v1.0.0-<timestamp>?pretty"` (where `<timestamp>` is the one of the index)

## 3. Files
The files are saved on the container `fare-invenio_web-ui_1` in the directory `/opt/invenio//var/instance/data/`. To make the files backup just run a `docker cp <src> <dest>` command, to copy the files from the container to the host.

## 4. Scripts

The backup and restore procedures described above are automated by two scripts.

### 4.1 Backup script

The backup script can be run every time you want to save the current state of the platform. 
The script:
- Creates the directory where to store the backup if not present.
- Makes the dump of the metadata, overwriting the old one.
- Checks if the repo is already registered or not, if not it creates the repo.
- Saves the snapshot of the indexes, with a progressive number.
- Copies the dump of the indexes and the files in the host.

To execute the script run the command `pipenv run ./scripts/backup`

### 4.2 Restore script

The restore script can be run when you need to restore your data from a backup.
The script:
- Copies the dump files from the host to the different containers.
- Makes the restore of the metadata.
- Checks if the repo is already registered or not, if not it creates the repo.
- Closes the `.kibana` index if present.
- Calculates the number of the snapshot to restore, taking the more recent one.
- Retrieves all the elasticsearch indexes in the form of `records-record-v1.0.0-<timestamp>` and delete all the indexes with the `<timestamp>` most recent

To execute the script run the command `pipenv run ./scripts/restore`
