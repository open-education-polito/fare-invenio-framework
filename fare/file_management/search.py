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


class AdvancedSearch(RecordsSearch):
    """Define default filter for search records with the selected fields."""

    class Meta:
        """Configuration for search."""

        index = '_all'
        doc_types = None
        fields = ('*', )
        facets = {}

    def __init__(self, d, **kwargs):
        """Init for AdvancedSearch."""
        super(AdvancedSearch, self).__init__(**kwargs)

        
        print('-------------INIT-ADV--SRC---------------')
        print(d)

        self.query = Q(
            Bool(filter=[
                        Q('term', title=d['title']),
                        Q('term', contributors=d['contributors']),
                        Q('term', educationLevel=d['educationLevel']),
                        Q('term', subject=d['subject']),
                        Q('term', converage=d['coverage']),
                        Q('term', revisioned=True)
                        ]
                 )
        )
