# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Default configuration for fare.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""
from __future__ import absolute_import, print_function
import os
from dotenv import load_dotenv
from datetime import timedelta
import invenio_logging.config


def _(x):
    """Identity function used to trigger string extraction."""
    return x

# Loading dotenv
load_dotenv()


# Logging 
# =======
#: Handling logging configurations
# Exceptions are not catched, fail fast fail often

LOGGING_PATH = os.getenv('LOGGING_PATH') or "/var/logs/fare/fare.log"
os.makedirs(os.path.dirname(LOGGING_PATH), exist_ok=True)
invenio_logging.config.LOGGING_FS_LOGFILE = LOGGING_PATH
invenio_logging.config.LOGGING_FS_PYWARNINGS = True

# Rate limiting
# =============
#: Storage for ratelimiter.
RATELIMIT_STORAGE_URL = 'redis://localhost:6379/3'

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'it'
BABEL_DEFAULT_LOCALE = 'it'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Rome'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    # ('fr', _('French'))
]

# Base templates
# ==============
#: Global base template.
BASE_TEMPLATE = 'fare/page.html'
#: Cover page base template (used for e.g. login/sign-up).
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
#: Footer base template.
FOOTER_TEMPLATE = 'invenio_theme/footer.html'
#: Header base template.
HEADER_TEMPLATE = 'invenio_theme/header.html'
#: Settings base template.
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# Theme configuration
# ===================
APP_THEME = ['bootstrap3']
#: Site name
THEME_SITENAME = _('FARE')
#: Use default frontpage.
THEME_FRONTPAGE = True
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('Esplora. Collabora. Impara.')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'fare/frontpage.html'
#: Theme logo.
THEME_LOGO = 'images/fare_logo.png'
#: Site images.
SITE_IMAGES = 'images/'

# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "fare@polito.it"
#: Disable email sending by default.
MAIL_SUPPRESS_SEND = True

# Assets
# ======
#: Static files collection method (defaults to copying files).
COLLECT_STORAGE = 'flask_collect.storage.file'

# Accounts
# ========
#: Email address used as sender of account registration emails.
SECURITY_EMAIL_SENDER = SUPPORT_EMAIL
#: Email subject for account registration emails.
SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to FARE!")
#: Redis session storage URL.
ACCOUNTS_SESSION_REDIS_URL = 'redis://localhost:6379/1'
#: Enable session/user id request tracing. This feature will add X-Session-ID
#: and X-User-ID headers to HTTP response. You MUST ensure that NGINX (or other
#: proxies) removes these headers again before sending the response to the
#: client. Set to False, in case of doubt.
ACCOUNTS_USERINFO_HEADERS = True

# Celery configuration
# ====================

BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of message broker for Celery (default is RabbitMQ).
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#: URL of backend for result storage (default is Redis).
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#: Scheduled tasks configuration (aka cronjobs).
CELERY_BEAT_SCHEDULE = {
    'indexer': {
        'task': 'invenio_indexer.tasks.process_bulk_queue',
        'schedule': timedelta(minutes=5),
    },
    'accounts': {
        'task': 'invenio_accounts.tasks.clean_session_table',
        'schedule': timedelta(minutes=60),
    },
}

# Database
# ========
#: Database URI including user and password
SQLALCHEMY_USER = os.getenv('PG_USER')
SQLALCHEMY_PWD = os.getenv('PG_PASSWORD')
PG_DB = os.getenv('PG_DB')
SQLALCHEMY_DATABASE_URI = \
        'postgresql+psycopg2://' + SQLALCHEMY_USER + ':' + SQLALCHEMY_PWD + '@localhost/' + PG_DB

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'fare.polito.it'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = os.getenv('SECRET_KEY')
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 10 * 1024 * 1024 * 1024  # 10 GB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.
APP_ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if os.getenv('CURRENT_HOST') is not None:
    APP_ALLOWED_HOSTS.insert(0,os.getenv('CURRENT_HOST'))

# OAI-PMH
# =======
OAISERVER_ID_PREFIX = 'oai:fare.polito.it:'

# Debug
# =====
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available at
# https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration

#: Switches off incept of redirects by Flask-DebugToolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False

FIXTURES_FILES_LOCATION = 'data/'
"""Location where uploaded files are saved. If not an absolute path it is
   relative to instance path.
"""

FIXTURES_ARCHIVE_LOCATION = 'archive/'
"""Location where uploaded files are archived. If not an absolute path it is
   relative to instance path.
"""
