"""Views for file_management of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, abort, current_app, redirect, render_template, \
    request, url_for
from flask_babelex import gettext as _
from flask_login import login_required
from flask_menu import register_menu
from flask_security import current_user, roles_accepted
from invenio_files_rest.models import Bucket, ObjectVersion
from sqlalchemy.orm.exc import NoResultFound

from .api import RecordFare
from .forms import RecordForm
from .search import StatusSearch
from .utils import get_all_arguments, get_all_subjects, get_all_education_levels

# define a new Flask Blueprint that is register
# under the url path /file_management
blueprint = Blueprint(
    'file_management',
    __name__,
    url_prefix='/file_management',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/user_uploads', methods=('GET',))
@login_required
@register_menu(blueprint, 'settings.status',
               _('%(icon)s Stato files',
                 icon='<i class="fa fa-check-circle fa-fw"></i>'
                 ),
               order=6
               )
def user_uploads():
    """View to let user see the status (revisioned=true/false) of his files"""
    status = StatusSearch()
    return render_template('file_management/user_uploads.html', records_list=status.execute().hits)


@blueprint.route('/arguments', methods=('GET',))
def retrieve_arguments():
    return get_all_arguments()


@blueprint.route('/search_page', methods=('GET',))
def search_page():
    return render_template('file_management/search_page.html')


@blueprint.route('/info_create', methods=('GET',))
def info_create():
    return render_template('file_management/info_create.html')


@blueprint.route('/guide_search', methods=('GET',))
def retrieve_guide_search():
    subjects = get_all_subjects()
    education_levels = get_all_education_levels()
    return render_template('file_management/guide_search.html', subjects=subjects, education_levels=education_levels)


@blueprint.route('/guide_permissions', methods=('GET',))
def retrieve_guide_permissions():
    return render_template('file_management/guide_permissions.html')


@blueprint.route('/guide_upload', methods=('GET',))
def retrieve_guide_upload():
    return render_template('file_management/guide_upload.html')


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
@register_menu(blueprint, 'settings.createfile',
               _('%(icon)s Carica file',
                 icon='<i class="fa fa-file-text fa-fw"></i>'
                 ),
               order=5
               )
def create():
    """The create view."""
    form = RecordForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        list_names = form.contributor_name.data.split(",")
        list_contributors = []

        for contributor in list_names:
            t = {"name": contributor}
            list_contributors.append(t)

        # we creare contributors object with the submitted names
        contributors = list_contributors
        # set the owner as the current logged in user
        owner = int(current_user.get_id())
        # set the school order
        educationLevel = form.educationLevel.data
        # set the discipline
        subject = form.subject.data
        # set the argument
        coverage = form.coverage.data
        # set the license
        license = form.license.data
        # set the description
        description = form.description.data
        # set the file of the record
        content = form.file_content.data
        # create the record and set the revisioned field to false
        RecordFare.create_record(
          dict(
            title=form.title.data,
            contributors=contributors,
            owner=owner,
            educationLevel=educationLevel,
            subject=subject,
            coverage=coverage,
            license=license,
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
@roles_accepted('admin', 'staff')
@register_menu(blueprint, 'settings.revision',
               _('%(icon)s Revisione contenuti',
                   icon='<i class="fa fa-eye fa-fw"></i>'),
               order=6,
               visible_when=lambda: bool(current_user.has_role('admin') or
                                         current_user.has_role('staff')
                                         ) is not False
               )
def revision_list():
    """View to display all unrevisioned records."""
    return render_template('file_management/unrevisioned.html')


@blueprint.route('/publish/', methods=('GET', 'POST'))
@login_required
def publish():
    """View to publish a record."""
    record_id = request.form['record_id']

    # retrieve the record
    try:
        record = RecordFare.get_record(record_id)
    except NoResultFound:

        current_app.logger.error(
                            "Impossible to publish file requested by user= " +
                            current_user.email + " ,record id not found: " +
                            record_id
                                )
        abort(404)

    RecordFare.publish_record(record)

    return render_template('file_management/unrevisioned.html')


@blueprint.route('/delete/', methods=('GET', 'POST'))
@login_required
def delete():
    """The delete view."""
    bucket_uuid = request.form['record_bucket']
    record_id = request.form['record_id']

    # get Bucket object
    bucket = Bucket.get(bucket_uuid)

    # chekc if the bucket exist
    if bucket is None:
        current_app.logger.error(
                        "Impossible to delete the file requested by user= " +
                        current_user.email + ", bucket not found: " +
                        bucket_uuid
        )
        abort(404)

    # store buckets values: version_id and the key
    values = str(bucket.objects[0]).split(':')
    version_id = values[1]
    key = values[2]
    # retrieve the fileinstance_id
    fileinstance_id = str(ObjectVersion.get(bucket, key, version_id).file_id)

    # creating MyRecord object, extention of invenio_records_files.Record
    try:
        record = RecordFare.get_record(record_id)
    except NoResultFound:

        current_app.logger.error(
                            "Impossible to delete file requested by user= " +
                            current_user.email + " ,record id not found: " +
                            record_id
                                )
        abort(404)

    # check if the user is the owner of the record or if is admin or staff
    if(
            (not current_user.id == record['owner']) and
            (not current_user.has_role('admin')) and
            (not current_user.has_role('staff'))
    ):
        current_app.logger.error(
                            "Impossible to delete file requested by user= " +
                            current_user.email + " , this user does not have \
                            the permission, action not allowed"
                                )
        abort(403)

    record.delete_record(fileinstance_id, record_id)
    return redirect(url_for('file_management.success_delete'))


@blueprint.route('/download/', methods=('GET', 'POST'))
def download():
    """The download view."""
    # storing the bucket uuid
    bucket_uuid = request.form['record_bucket']
    record_id = request.form['record_id']

    # check if the session is anonymous or not
    if not hasattr(current_user, 'email'):
        usr = "anonymous"
    else:
        usr = current_user.email

    # get Bucket object
    bucket = Bucket.get(bucket_uuid)

    # chekc if the bucket exist
    if bucket is None:
        current_app.logger.error(
                            "Impossible to download file requested by user= " +
                            usr + ", bucket not found: " + bucket_uuid
                                )
        abort(404)

    # store buckets values: bucket, version_id and the key
    values = str(bucket.objects[0]).split(':')
    bucket = values[0]
    version_id = values[1]
    key = values[2]

    try:
        record = RecordFare.get_record(record_id)
    except NoResultFound:

        current_app.logger.error(
                            "Impossible to download file requested by user= " +
                            usr + " ,record id not found: " + record_id
                                )
        abort(404)

    # check if the file is revisioned, if not only
    # staff member can download it to do the review
    if not record['revisioned']:
        if (
            (not current_user.has_role('admin')) and
            (not current_user.has_role('staff'))
        ):

            current_app.logger.error(
                            "Impossible to download file= " + record['title'] +
                            ", user= " + usr + " not authorized"
                                    )

            # forbidden for the user
            abort(403)

    return RecordFare.download_record(record, bucket, key, version_id, usr)


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
