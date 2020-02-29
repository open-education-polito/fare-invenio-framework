# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Searching class for revisioned records."""

from __future__ import absolute_import, print_function

from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from invenio_search.api import RecordsSearch


class RevisionedRecordsSearch(RecordsSearch):
    """Define default filter for search revisioned record."""

    class Meta:
        """Configuration for search."""

        index = '_all'
        doc_types = None
        fields = ('*', )
        facets = {}

    def __init__(self, **kwargs):
        """Init class for RevisionedRecordsSearch."""
        super(RevisionedRecordsSearch, self).__init__(**kwargs)
        self.query = Q(
            Bool(filter=[Q('term', revisioned=True)])
        )
