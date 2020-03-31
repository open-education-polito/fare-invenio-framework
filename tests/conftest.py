# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.models import Role
from invenio_app.factory import create_app
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_files_rest import InvenioFilesREST
from invenio_records import InvenioRecords
from invenio_userprofiles import InvenioUserProfiles, UserProfile
from invenio_userprofiles.views import blueprint_ui_init
from sqlalchemy_utils.functions import create_database, database_exists


@pytest.fixture
def app():
    """Create fixture app."""
    # Set temporary instance path for sqlite
    instance_path = tempfile.mkdtemp()
    _app = Flask('testapp', instance_path=instance_path)
    InvenioAccess(_app)
    InvenioAccounts(_app)
    InvenioDB(_app)
    InvenioUserProfiles(_app)
    InvenioRecords(_app)
    InvenioFilesREST(_app)
    # UserProfile(_app)

    _app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
        TESTING=True,
        SECRET_KEY='test',
    )

    with _app.app_context():
        yield _app

    # Teardown instance path.
    shutil.rmtree(instance_path)


@pytest.fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()

    yield db_

    db_.session.remove()
    db_.drop_all()


@pytest.fixture
def client(app, db):
    """Create fixture client."""
    _client = app.test_client()
    return _client


@pytest.fixture()
def users(db, app):
    """Create admin, staff and user."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore

        # create users
        staff = datastore.create_user(
            email="staff@test.com", password="123456", active=True
        )
        admin = datastore.create_user(
            email="admin@test.com", password="123456", active=True
        )
        user = datastore.create_user(
            email="user@test.com", password="123456", active=True
        )

        # Give role to admin and add to db
        admin_role = Role(name="admin")
        datastore.add_role_to_user(admin, admin_role)
        db.session.add(admin)

        # Give role to user and add to db
        staff_role = Role(name="staff")
        datastore.add_role_to_user(staff, staff_role)
        db.session.add(staff)

        # add user to db
        db.session.add(user)

    db.session.commit()

    return {"admin": admin, "staff": staff, "user": user}


'''
def _init_userprofiles(app):
    """Init userprofiles module."""
    InvenioUserProfiles(app)
    app.register_blueprint(blueprint_ui_init)
    return app


@pytest.fixture
def app_with_userprofiles(app):
    """Configure userprofiles module with CSRF disabled."""
    app.config.update(
        USERPROFILES_EXTEND_SECURITY_FORMS=True,
        WTF_CSRF_ENABLED=False,
    )
    return _init_userprofiles(app)


@pytest.fixture()
def user_temp(app_with_userprofiles):
    """Create user."""
    with db.session.begin_nested():
        datastore = app_with_userprofiles.extensions['security'].datastore
        user1 = datastore.create_user(email='info@inveniosoftware.org',
                                      password='tester', active=True)
        profile = UserProfile(username='mynick', user=user1)
        db.session.add(profile)
    db.session.commit()
    return user1
'''
