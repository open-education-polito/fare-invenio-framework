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
        'fare-frontpage': './scss/fare/frontpage.scss',
        'fare-footer': './scss/fare/footer.scss',
        'fare-search-page': './scss/fare/search-page.scss',
        'status-files': './scss/fare/status-files.scss',
        'guide': './scss/fare/guide.scss',
        'fare-argument': './js/fare/argument.js',
    },
    dependencies={
        # add any additional npm dependencies here...
    }
)
