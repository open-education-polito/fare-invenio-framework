# 3. Log messages

Date: 2020-08-16

## Status

Accepted

## Context

The staging and deployment strategy has to change. Right now many different
services are loaded, there is confusion regarding what to use and when. We need
a simpler way of handling such deployment. 

## Decision

Change the deployment. We want to have only the services in use exposed.
Moreover, we should automatize the overall process.

## Consequences

A new file, called docker-compose.fare.yml has been inserted.
