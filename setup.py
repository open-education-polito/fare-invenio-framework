# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Free Architecture for Remote Education"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('fare', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='fare',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='fare Invenio',
    license='MIT',
    author='Open Education Polito',
    author_email='fare@polito.it',
    url='https://github.com/open-education-polito/fare-platform',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'fare = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'fare_records = fare.records:fare',
        ],
	'flask.commands': [
    	    'locations = fare.records.cli:locations',
	],
        'invenio_base.blueprints': [
            'fare = fare.theme.views:blueprint',
            'fare_records = fare.records.views:blueprint',
            'fare_grant_roles = fare.grant_roles.views:blueprint',
	    'fare_file_management = fare.file_management.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'fare_theme = fare.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'fare = fare.config',
        ],
        'invenio_i18n.translations': [
            'messages = fare',
        ],
        'invenio_base.api_apps': [
            'fare = fare.records:fare',
         ],
        'invenio_jsonschemas.schemas': [
            'fare = fare.records.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = fare.records.mappings'
        ],
        "invenio_pidstore.minters": [
            "fmgid = fare.file_management.api:file_management_pid_minter",
        ],
        "invenio_pidstore.fetchers": [
            "fmgid = fare.file_management.api:file_management_pid_fetcher",
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
