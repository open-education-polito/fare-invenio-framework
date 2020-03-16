"""Views for file_management of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import login_required
from flask_security import current_user
from invenio_files_rest.models import Bucket, ObjectVersion

from .api import create_record, delete_record, publish_record
from .forms import RecordForm
from .models import MyRecord

# define a new Flask Blueprint that is register
# under the url path /file_management
blueprint = Blueprint(
    'file_management',
    __name__,
    url_prefix='/file_management',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """The create view."""
    form = RecordForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        # we creare one contributor object with the submitted name
        contributors = [dict(name=form.contributor_name.data)]
        # set the owner as the current logged in user
        owner = int(current_user.get_id())
        # set the school order
        educationLevel = form.educationLevel.data
        # set the discipline
        subject = form.subject.data
        # set the argument
        coverage = form.coverage.data
        # set the description
        description = form.description.data
        # set the file of the record
        content = form.file_content.data
        # create the record and set the revisioned field to false
        create_record(
          dict(
            title=form.title.data,
            contributors=contributors,
            owner=owner,
            educationLevel=educationLevel,
            subject=subject,
            coverage=coverage,
            description=description,
            revisioned=False,
          ),
          content
        )
        # redirect to the success page
        return redirect(url_for('file_management.success'))
    return render_template('file_management/create.html', form=form)


@blueprint.route('/revision/', methods=('GET',))
@login_required
def revision_list():
    """View to display all unrevisioned records."""
    # check if the user is admin or staff
    if(
            (not current_user.has_role('admin')) and
            (not current_user.has_role('staff'))
    ):
        abort(403)

    return render_template('file_management/unrevisioned.html')


@blueprint.route('/publish/', methods=('GET', 'POST'))
@login_required
def publish():
    """View to publish a record."""
    record_id = request.form['record_id']
    # retrieve the record
    record = MyRecord.get_record(record_id)
    publish_record(record)

    return render_template('file_management/unrevisioned.html')


@blueprint.route('/delete/', methods=('GET', 'POST'))
@login_required
def delete():
    """The delete view."""
    bucket_uuid = request.form['record_bucket']
    record_id = request.form['record_id']

    # get Bucket object
    bucket = Bucket.get(bucket_uuid)
    # store buckets values: version_id and the key
    values = str(bucket.objects[0]).split(':')
    version_id = values[1]
    key = values[2]
    # retrieve the fileinstance_id
    fileinstance_id = str(ObjectVersion.get(bucket, key, version_id).file_id)
    # creating MyRecord object, extention of invenio_records_files.Record
    record = MyRecord.get_record(record_id)
    # check if the user is the owner of the record or if is admin or staff
    if(
            (not current_user.id == record['owner']) and
            (not current_user.has_role('admin')) and
            (not current_user.has_role('staff'))
    ):
        abort(403)

    delete_record(fileinstance_id, version_id, record_id, record)
    return redirect(url_for('file_management.success_delete'))


@blueprint.route("/success")
@login_required
def success():
    """The success view."""
    return render_template('file_management/success.html')


@blueprint.route("/success_delete")
@login_required
def success_delete():
    """The success view."""
    return render_template('file_management/success_delete.html')
