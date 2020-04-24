# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

# import json
#
# import requests
# from flask_security import current_user, login_user


# def test_unknown_upload_record_file(app, users):
#     """
#     Test purpose:
#     upload a file with the respective metadata
#
#     Input:
#     not authenticated user
#
#     Output:
#     POST with status code 200
#     """
#     url = "https://localhost:5000/file_management/create"
#     data = {}
#     data['file_content'] = "Hello"
#     data['title'] = "Test title"
#     data['contributor_name'] = "Test contributor"
#     data['educationLevel'] = "Test level"
#     data['subject'] = "Test subject"
#     data['coverage'] = "Test coverage"
#     data['description'] = "Test description"
#
#     r = requests.post(url, data=data, verify=False, allow_redirects=False)
#     assert r.status_code == 302
#
#     record_url = "https://localhost:5000/records/1"
#     r = requests.get(record_url, verify=False)
#     assert r.status_code == 404


# def test_admin_upload_record_file(app, users, db):
#     """
#     Test purpose:
#     upload a file with the respective metadata
#
#     Input:
#     authenticated user
#
#     Output:
#     POST with status code 200
#     """
#     url = "https://localhost:5000/file_management/create"
#     data = {}
#     data['file_content'] = "Hello"
#     data['title'] = "Test title"
#     data['contributor_name'] = "Test contributor"
#     data['educationLevel'] = "Test level"
#     data['subject'] = "Test subject"
#     data['coverage'] = "Test coverage"
#     data['description'] = "Test description"
#
#     admin = users['admin']
#     login_user(admin)
#
#     r = requests.post(url, data=data, verify=False)
#     assert r.status_code == 200
#
#     record_url = "https://localhost:5000/records/1"
#     r = requests.get(record_url, verify=False)
#     assert r.status_code == 200
