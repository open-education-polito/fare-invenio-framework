"""MyRecord class model."""

from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets


class MyRecord(Record):
    """MyRecord class."""

    def delete(self, force=True):
        """Delete function for a record."""
        # Remove links between records and buckets
        RecordsBuckets.query.filter_by(
                bucket=self.files.bucket
        ).delete()

        # Remove bucket and all associated object versions.
        self.bucket.remove()

        return super(Record, self).delete(force=force)
