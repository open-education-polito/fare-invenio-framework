# Backup and restore FARE

The backup is composed of three parts:
- Databse where are stored all the metadata and the users
- Elasticsearch which is used to index the records and search them
- Files which should be stored in a shared volume

## 0. Shared volumes

Data are shared between containers and host, they was added in the `docker-compose.full.yml` file and are organazied as follow:
- To share the dump of the metadata between the `fare-invenio_db_1` container and the host, it was added  `/fare_shared_data/fare_db:/backup_fare_db` as volume in the `db` section
- To share the dump of the indexes between the `fare-invenio_es_1` container and the host, it was added `/fare_shared_data/fare_es:/usr/share/elasticsearch/backup_fare_es` as volume in the `es` section
- `/fare_shared_data/fare_files:/opt/invenio/instance/data/` was added in the `web-ui` section, to share the files uploaded in the platform

## 1. Database
The dump of the metadata and the users can be done with this command:
```
docker exec fare-invenio_db_1 pg_dumpall -U fare > ~/fare_shared_data/fare_db/backup_fare_db.sql
```
Where:
- `fare-invenio_db_1` is the name of the container
- `pg_dumpall` the command of postgres to dump all the database
- `-U fare` the user
- `~/fare_shared_data/fare_db/backup_fare_db.sql` the path where to save the dump

Doing so we will have the dump of the database in the `/backup_fare_db` in the `fare-invenio_db_1` container and in the `~/fare_shared_data/fare_db/` path in the host.

To restore the data we have to run this command:
```
docker exec fare-invenio_db_1 psql -f /backup_fare_db/backup_fare_db.sql -U fare
```

Where:
- `fare-invenio_db_1` is the name of the container
- `psql` the command of postgres to restore the data
- `-f /backup_fare_db/backup_fare_db.sql` the file where there is the dump of the database
- `-U fare` the user

## 2. Elasticsearch
First of all the path where to store the dump must be specified in the config file, it was done modifing the config file of elasticsearch in  `/docker/elasticsearch/elasticsearch.yml` adding the path of the repo `path.repo: ["<path_where_to_store_the_dump>"]`, doing so it's not needed to stop and restart the container.

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
- `curl -X POST http://localhost:9200/_snapshot/prova_backup/snapshot_1/_restore`
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
The files are saved in the container `fare-invenio_web-ui_1` in the directory `/opt/invenio/instance/data/` to make the backup of the files, you have to specify the shared volume in the `docker-compose.full.yml` file, at the `web-ui` section.

## 4. Scripts

The procedure of backup and restore of the data described above was automated by two scripts.

### 4.1 backup script

The backup script can be run every time you want to save the current state of the platform. 
The script:
- Make the dump of the metadata, overwriting the old one.
- Check if the repo is yet registered or not, if not it creates the repo.
- Save the snapshot of the indexes, with a progressive number.

### 4.2 restore script

The restore script can be run when you need to restore your data from a backup.
The script:
- Make the restore of the metadata.
- Check if the repo is yet registered or not, if not it creates the repo.
- Close the `.kibana` index.
- Calculate the number of the snapshot to restore, taking the one more recent.
- Retrieve all the elasticsearch indexes in the form of `records-record-v1.0.0-<timestamp>` and deleting all the indexes with the `<timestamp>` most recent