# 2. Permission crud operations on records config

Date: 2020-02-25

## Status

Accepted

## Context

Initially a record could be made by anyone, but the problem is that that record was only some metadata without file attached on it.

## Decision

To avoid the situation where a record is created without file, we put `deny_all` permission in fare/records/config.py that denies to all the possibilities to create, update and delete this kind of records.

## Consequences

In this way no one can create a record with only the metadata on it and without file attached.
