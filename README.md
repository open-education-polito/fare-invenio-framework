![https://travis-ci.org/open-education-polito-it/fare-invenio](https://img.shields.io/travis/open-education-polito/fare-invenio.svg)
![https://coveralls.io/r/open-education-polito/fare-invenio](https://img.shields.io/coveralls/open-education-polito/fare-invenio.svg)
![https://github.com/open-education-polito/fare-invenio/blob/master/LICENSE](https://img.shields.io/github/license/open-education-polito/fare-invenio.svg)
[![GitHub release](https://img.shields.io/github/release/open-education-polito/fare-invenio.svg?style=plastic)](https://github.com/open-education-polito/fare-invenio/releases)

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

This project runs Invenio v3.2.1. 

## Prerequisites

To be able to develop and run out instance you will need the following installed and configured on your system:

* [Docker v1.18+](https://docs.docker.com/install/) and [Docker Compose v1.23+](https://docs.docker.com/compose/install/)
* [NodeJS v6.x+ and NPM v4.x+](https://nodejs.org/en/download/package-manager/)
* [Enough virtual memory](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-cli-run-prod-mode) for Elasticsearch (when running in Docker), if running Linux/MacOS you'll have to bump your `vm.max_map_count` as described in [Elasticsearch docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)
* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Installation

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

**Note:** because of the version of the `invenio-records-files` module that is not an official release, before execute the next point add the following line in the `/scripts/bootstrap` file, after the `pipenv sync --dev` line

```
pipenv run pip install --upgrade invenio-files-rest
```

Finally, install all dependencies, build the JS/CSS assets, create the database tables and create the Elasticsearch indices by running the bootstrap and setup scripts:

```
(my-site)$ ./scripts/bootstrap
(my-site)$ ./scripts/setup
```

Remeber to install also the `invenio-records-files` module:

```
(my-site)$ pip install invenio-records-files
```

## Run

You can now start the development web server and the background worker for your new instance:

```
(my-site)$ ./scripts/server
* Environment: development
* Debug mode: on
* Running on https://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Code of conduct
[Code of conduct](https://www.contributor-covenant.org/)

## Reporting a bug and asking help

If you found a bug please report it [here](https://github.com/open-education-polito/fare-invenio) opening an issue.
Searching [help](https://github.com/open-education-polito/fare-invenio)?

## Semantic Versioning
[Here](https://semver.org/) the semantic versioning we use

# Maintenance
Code actually maintained by Open Education Polito.
For inquiries, please open an issue and tag @libremente.

# Logging
Logging is done by [invenio_loggigng](https://invenio-logging.readthedocs.io/en/latest/index.html) module.
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
