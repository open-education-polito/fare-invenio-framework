[![Build Status](https://travis-ci.org/open-education-polito/fare-platform.svg?branch=master)](https://travis-ci.org/open-education-polito/fare-platform)
[![Coverage Status](https://coveralls.io/repos/github/open-education-polito/fare-platform/badge.svg?branch=master)](https://coveralls.io/github/open-education-polito/fare-platform?branch=master)![https://github.com/open-education-polito/fare-platform/blob/master/LICENSE](https://img.shields.io/github/license/open-education-polito/fare-platform.svg)
[![GitHub release](https://img.shields.io/github/release/open-education-polito/fare-platform.svg?style=plastic)](https://github.com/open-education-polito/fare-platform/releases)

# FARE
> The Free Architecture for Remote Education

# Index
- [Introduction](#introduction)
- [How to contribute](#how-to-contribute)
- [Maintenance](#Maintenance)
- [License](#license)

# Introduction 
This is the main codebase for FARE. FARE is an e-learning web platform. The
main aim of FARE is to provide repository features: easy search and download
functionalities. 
Furthermore, for registered users it is possible to upload new contents, modify
some existing ones or delete. 

## Features list
* Quick search 
* Download simple Learning Object
* User login and permission management
* Content upload

## Searching material
To search the desired material you just have to type what you are looking for
in the search bar

## Upload content
Everyone can upload content but it is necessary to be logged in. After the upload your
content will be reviewed and, if everything is ok, it will be published. 

## Review the material
If you are a staff member, you can review the material and let it be visible by
everyone!

# How to contribute

This project runs Invenio v3.4.0. 

## Prerequisites

To be able to develop and run out instance you will need the following installed and configured on your system:

* [Docker v1.18+](https://docs.docker.com/install/) and [Docker Compose v1.23+](https://docs.docker.com/compose/install/)
* [NodeJS v6.x+ and NPM v4.x+](https://nodejs.org/en/download/package-manager/)
* [Enough virtual memory](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode) for Elasticsearch (when running in Docker), if running Linux/MacOS you'll have to bump your `vm.max_map_count` as described in [Elasticsearch docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)
* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Setting environment variables and volumes

**Important note:** Before run the application you need to:

* Set the environment variables in a `.env` file, it must be created. You can see an example in the `.env.example` file provided.

* Create the directories used as shared volumes to store the data used by the application executing the command:

	```
	$ pipenv run ./scripts/create-volumes
	```

## Production environment

### Run

You can use a full production environment using the
``docker-compose.fare.yml``. You can start it like this:

```
$ ./docker/build-images.sh
$ docker-compose -f docker-compose.fare.yml up -d
$ ./docker/wait-for-services.sh --full
```

Remember to create database tables, search indexes and message queues if not
already done:

```
$ docker-compose -f docker-compose.fare.yml run --rm web-ui ./scripts/setup
```

## Developement environment

### Installation

First, fire up the database, Elasticsearch, Redis and RabbitMQ:

```
$ cd my-site/
$ docker-compose up -d
Creating mysite_cache_1 ... done
Creating mysite_db_1    ... done
Creating mysite_es_1    ... done
Creating mysite_mq_1    ... done
```

Next, activate the virtualenv of the new project by running:

```
$ pipenv shell
```


Finally, install all dependencies, build the JS/CSS assets, create the database tables and create the Elasticsearch indices by running the bootstrap and setup scripts:

```
(my-site)$ ./scripts/bootstrap
(my-site)$ ./scripts/setup
```

### Run

You can now start the development web server and the background worker for your new instance:

```
(my-site)$ ./scripts/server
* Environment: development
* Debug mode: on
* Running on https://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Invenio documentation

Further documentation, related to the framework used and the topics not covered in this guide, can be found [here](https://invenio.readthedocs.io/en/latest/).

## Code of conduct
[Code of conduct](https://www.contributor-covenant.org/)

## Reporting a bug and asking help

If you found a bug please report it [here](https://github.com/open-education-polito/fare-platform) opening an issue.
Searching [help](https://github.com/open-education-polito/fare-platform)?

## Semantic Versioning
[Here](https://semver.org/) the semantic versioning we use

# Maintenance
Code actually maintained by Open Education Polito.
For inquiries, please open an issue and tag @libremente.

## Decision record
The decisions regarding the architecture are recorded in the ADR folder. Please
visit [ADR](docs/architecture/decisions) to know more about the previous
decisions.

# Logging
Logging is done by [invenio_logging](https://invenio-logging.readthedocs.io/en/latest/index.html) module.
The log messages are:
```
current_app.logger.debug('Where am I?')
current_app.logger.info('Hello world!')
current_app.logger.warning('Be carefull with overlogging.')
current_app.logger.error('Connection could not be initialized.')
current_app.logger.exception('You should not divide by zero!')
```
The file where to write the log messages can be specified setting the variable `LOGGING_FS_LOGFILE`

# Please note
This version works only with `python 3.6.x`

# Authors
The CVS provides detailed info regarding who did what. 

# License
This code is licensed under a MIT License, v3. See the LICENSE.md file for
extended info, and the license files inside each module's repository.
