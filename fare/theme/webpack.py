# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from __future__ import absolute_import, print_function

from flask_webpackext import WebpackBundle

theme = WebpackBundle(
    __name__,
    'assets',
    entry={
        'fare-theme': './scss/fare/theme.scss',
        'fare-argument': './js/fare/argument.js',
        'fare-advanced-search-argument': './js/fare/advanced_search_argument.js',
        'status-files': './scss/fare/status-files.scss',
        'guide': './scss/fare/guide.scss',
    },
    dependencies={
        # add any additional npm dependencies here...
    }
)
