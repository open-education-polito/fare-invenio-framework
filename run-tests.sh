#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.


pipenv check && \
pipenv run pydocstyle fare tests docs && \
pipenv run isort -rc -c -df && \
pipenv run check-manifest --ignore "docs/_build*" && \
pipenv run sphinx-build -qnNW docs docs/_build/html && \
pipenv run test
