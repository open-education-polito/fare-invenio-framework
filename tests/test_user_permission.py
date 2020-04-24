# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

import json

import requests
from flask_security import current_user, login_user


def test_anonymous_user_get_page(app):
    """
    Test purpose:
    an anonymous user perform a GET to the view for granting permissions

    Input:
    non authenticated user

    Output:
    GET of the permission page to change permission with status code 302
    """

    url = "https://localhost:5000/grant_staff/grant"
    r = requests.get(url, verify=False, allow_redirects=False)
    assert r.status_code == 302


def test_staff_get_page(app, users):
    """
    Test purpose:
    a user with staff permission can perform a GET
    to change permission page

    Input:
    one user who perform a GET with staff permission
    to the change staff permission page

    Output:
    GET return grant permission page with status code 200
    """

    url = "https://localhost:5000/grant_staff/grant"
    staff = users['staff']
    login_user(staff)
    r = requests.get(url, verify=False)
    assert r.status_code == 200


def test_staff_grant_user(app, users, db):
    """
    Test purpose:
    staff member perform a POST to change permission of
    another user without staff permission

    Input:
    two user, one who perform a POST with staff permission
    the other without it

    Output:
    GET change permission page of the requested user with status code 200
    """

    url = "https://localhost:5000/grant_staff/grant"
    staff = users['staff']
    user = users['user']
    login_user(staff)

    payload = {'email': user.email}

    r = requests.post(url, data=payload, verify=False)

    '''
    with client:
        r = client.post(json={
                'email': user_email
            }, follow_redirects=True
        )
        logging.debug(r)
        print(r.get_json())
    '''
    assert r.status_code == 200

    login_user(user)
    url = "https://localhost:5000/grant_staff/grant"
    r = requests.get(url, verify=False)
    assert r.status_code == 200

'''
def test_staff_grant_non_existing_user(app, users, db):
    """
    Test purpose:
    staff member perform a POST to change permission of
    another user that does not exist

    Input:
    one user who perform a POST with staff permission
    and a email that does not exist

    Output:
    perform a POST to permission view with status code 404
    """

    url = "https://localhost:5000/grant_staff/grant"
    staff = users['staff']
    user_email = "nonexistinguser@test.com"
    login_user(staff)
    payload = {'email': user_email}

    r = requests.post(url, data=payload, verify=False)

    """
    with client:
        r = client.post(url, json={
                'email': user_email
            }, follow_redirects=True
        )
    """
    assert r.status_code == 404


def test_admin_grant_staff(app, users, client, db):
    """
    Test purpose:
    admin member perform a POST to change permission of
    another staff user

    Input:
    one user who perform a POST with admin permission
    and a email of a staff user

    Output:
    perform a POST to permission view with status code 409
    """
    url = "https://localhost:5000/grant_staff/grant"
    admin = users['admin']
    user_email = users['staff'].email
    login_user(admin)
    payload = {'email': user_email}

    r = requests.post(url, data=payload, verify=False, allow_redirects=True)
    """
    with client:
        r = client.post(url, json={
                'email': user_email
            }, follow_redirects=True
        )
    """
    assert r.status_code == 409
'''
