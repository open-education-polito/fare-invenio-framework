from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from flask_security import current_user

from invenio_search.api import RecordsSearch


class RevisionSearch(RecordsSearch):
    """Define default filter for search unrevisioned record."""

    class Meta:
        """Configuration for search."""

        index = '_all'
        doc_types = None
        fields = ('*', )
        facets = {}

    def __init__(self, **kwargs):
        """Init for RevisionSearch."""
        super(RevisionSearch, self).__init__(**kwargs)
        self.query = Q(
            Bool(filter=[Q('term', revisioned=False)])
        )


class StatusSearch(RecordsSearch):
    """Define default filter for search records of a specific owner."""

    class Meta:
        """Configuration for search."""

        index = '_all'
        doc_types = None
        fields = ('*', )
        facets = {}

    def __init__(self, **kwargs):
        """Init for RevisionSearch."""
        super(StatusSearch, self).__init__(**kwargs)
        self.query = Q(
            Bool(filter=[Q('term', owner=current_user.id)])
        )
