"""file_management APIs."""

from __future__ import absolute_import, print_function

import shutil
import uuid
from functools import partial

from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from invenio_db import db
from invenio_files_rest.models import FileInstance
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records_files.api import Record
from invenio_search.api import RecordsSearch

from .fetchers import pid_fetcher
from .minters import dummy_pid_minter

FILE_MNGT_PID_TYPE = "fmgid"
FILE_MNGT_PID_MINTER = "fmgid"
FILE_MNGT_PID_FETCHER = "fmgid"

FileManagementIdProvider = type(
    'DocumentIdProvider',
    (RecordIdProviderV2,),
    dict(pid_type=FILE_MNGT_PID_TYPE, default_status=PIDStatus.REGISTERED)
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


def publish_record(record):
    """Revision a record."""
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
    # the full path is /home/<user>/.local/share/virtualenvs/
    # fare-invenio-<code>/var/instance/data/<f1>/<f2>/<bucketid>/<filename>
    # after have stored the index of the folder "data", where there are all
    # the records, the path is passed to the function below
    # and trimmed at <f1>, a folder name composed by 2 character,
    # at the index "i" is added 8 because is the number of
    # character for completing the path, terminating at "<f1>/"
    shutil.rmtree(uri[:i+8])
