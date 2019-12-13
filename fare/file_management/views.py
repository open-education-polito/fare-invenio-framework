"""Views for file_management of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for, abort
from flask_login import login_required
from flask_security import current_user, roles_accepted

from .forms import RecordForm, DeleteForm
from .api import create_record, delete_record
from flask import request

from .models import MyRecord
from invenio_files_rest.models import Bucket, ObjectVersion

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
        school_order = form.school_order.data
        # set the discipline
        discipline = form.discipline.data
        # set the argument
        argument = form.argument.data
        # set the description
        description = form.description.data
        # set the file of the record
        content = form.file_content.data
        # create the record
        create_record(
          dict(
            title=form.title.data,
            contributors=contributors,
            owner=owner,
            school_order=school_order,
            discipline=discipline,
            argument=argument,
            description=description,
          ),
          content
        )
        # redirect to the success page
        return redirect(url_for('file_management.success'))
    return render_template('file_management/create.html', form=form)


@blueprint.route('/delete/', methods=('GET', 'POST'))
@login_required
def delete():
    """The delete view."""

    form = DeleteForm()

    # storing the bucket uuid
    if request.method == 'GET':
        bucket_uuid = request.args.get('record_bucket')
    else:
        bucket_uuid = form.file_bucket.data

    # get Bucket object
    bucket = Bucket.get(bucket_uuid)
    # store buckets values: version_id and the key
    values = str(bucket.objects[0]).split(':')
    version_id = values[1]
    key = values[2]
    # retrieve the fileinstance_id
    fileinstance_id = str(ObjectVersion.get(bucket, key, version_id).file_id)
    # creating MyRecord object, extention of invenio_records_files.Record
    record = MyRecord.get_record(key)

    # check if the user is the owner of the record or if is admin or staff
    if(
            (not current_user.id == record['owner']) and
            (not current_user.has_role('admin')) and
            (not current_user.has_role('staff'))
    ):
        abort(403)

    if form.validate_on_submit():
        delete_record(fileinstance_id, version_id, key, record)
        return redirect(url_for('file_management.success_delete'))

    form.file_bucket.data = bucket_uuid

    return render_template('file_management/delete.html', form=form)


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
