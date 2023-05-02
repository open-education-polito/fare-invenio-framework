#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.


script_path=$(dirname "$0")

pipfile_lock_path="$script_path/../Pipfile.lock"

if [ ! -f $pipfile_lock_path ]; then
    echo "'Pipfile.lock' not found. Generate it by running 'pipenv lock'."
    exit 1
fi

# Extract Pipfile.lock hash to use as the docker image tag
deps_ver=$(cat $pipfile_lock_path | python3 -c "import json,sys;print(json.load(sys.stdin)['_meta']['hash']['sha256'])")

# Build dependencies image
docker build -f Dockerfile.base -t fare-base:$deps_ver .

# Build application image
docker build --build-arg DEPENDENCIES_VERSION=$deps_ver . -t fare
