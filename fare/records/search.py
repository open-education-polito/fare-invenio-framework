from __future__ import absolute_import, print_function

import uuid

from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records_files.api import Record


from invenio_search.api import RecordsSearch, DefaultFilter
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool


class RevisionedRecordsSearch(RecordsSearch):
    """Define default filter for search revisioned record."""

    class Meta:
        """Configuration for search."""

        # default_filter = DefaultFilter('revisioned:True')
        # default_filter = Q(True, field='record.revisioned')
        index = '_all'
        # doc_types = ['revisioned']
        doc_types = None
        fields = ('*', )
        facets = {}

    def __init__(self, **kwargs):
        super(RevisionedRecordsSearch, self).__init__(**kwargs)
        self.query = Q(
            Bool(filter=[Q('term', revisioned=True)])
        )

