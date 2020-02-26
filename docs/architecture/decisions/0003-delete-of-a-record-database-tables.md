# 2. Delete of a record, database tables

Date: 2020-02-26

## Status

Accepted

## Context

Completely delete a file is not an easy thing to do in invenio. To achieve this goal we tried to delete as many info as possible.

## Decision

Delete a record means delete it from the disk, from the database tables and not indexing it anymore. We decided to delete it from all the tables except `record_metadata_version`

## Consequences

In this way that table show all the operation (create and delete) made on a file, behaving like a log table in which there is all the file's history
