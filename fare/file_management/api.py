"""file_management APIs."""

from __future__ import absolute_import, print_function

import uuid

from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records_files.api import Record

from .models import MyRecord
from invenio_files_rest.models import Bucket, FileInstance, ObjectVersion
import shutil
from invenio_pidstore.models import PersistentIdentifier

from invenio_search.api import RecordsSearch, DefaultFilter
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool

# library for rest endpoint
from functools import partial
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from .fetchers import pid_fetcher
from .minters import dummy_pid_minter


FILE_MANAGEMENT_PID_TYPE = "fmgid"
FILE_MANAGEMENT_PID_MINTER = "fmgid"
FILE_MANAGEMENT_PID_FETCHER = "fmgid"

FileManagementIdProvider = type(
    'DocumentIdProvider',
    (RecordIdProviderV2,),
    dict(pid_type=FILE_MANAGEMENT_PID_TYPE, default_status=PIDStatus.REGISTERED)
)
file_management_pid_minter = dummy_pid_minter
file_management_pid_fetcher = partial(
    pid_fetcher,
    provider_cls=FileManagementIdProvider
)


def create_record(data, file_content):
    """Create a record.

    :param dict data: The record data.
    :param file_content: The file to store.
    """
    with db.session.begin_nested():

        # create uuid
        rec_uuid = uuid.uuid4()
        # create PID
        current_pidstore.minters['recid'](rec_uuid, data)
        # create record and the associated bucket
        created_record = Record.create(data, id_=rec_uuid)
        
        # index the record
        RecordIndexer().index(created_record)
        
        # store the file and link it to the metadata
        created_record.files[str(rec_uuid)] = file_content

    db.session.commit()


class RevisionSearch(RecordsSearch):
    """Define default filter for search unrevisioned record."""

    class Meta:
        """Configuration for search."""

        # default_filter = DefaultFilter('revisioned:True')
        # default_filter = Q(True, field='record.revisioned')
        index = '_all'
        # doc_types = ['unrevisioned']
        doc_types = None
        fields = ('*', )
        facets = {}


    def __init__(self, **kwargs):
        super(RevisionSearch, self).__init__(**kwargs)
        self.query = Q(
            Bool(filter=[Q('term', revisioned=False)])
        )


def publish_record(record):
    with db.session.begin_nested():

        record['revisioned'] = True
        record.commit()
        RecordIndexer().index(record)

    db.session.commit()


def delete_record(fileinstance_id, version_id, key, record):
    """Delete a record.

    :param dict data: The record data.
    :param file_content: The file to store.
    """

    # get the FileInstance object
    file_instance = FileInstance.get(fileinstance_id)
    # get the uri of the file for the directory of the folder
    uri = file_instance.uri
    # building the path to delete by storing the index of the folder data
    i = uri.find('data')

    # removing the record indexing, the record and the file instance
    recind = RecordIndexer()
    recind.delete_by_id(record_uuid=key)
    record.delete()
    FileInstance.query.filter_by(id=fileinstance_id).delete()
    PersistentIdentifier.query.filter_by(object_uuid=key).delete()
    db.session.commit()

    # removing the file on disk and the folder containing it
    shutil.rmtree(uri[:i+8])

