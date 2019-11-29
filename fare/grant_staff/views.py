"""Views for grant_staff permission to other users."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required
from flask_security import current_user

from .forms import StaffForm
from flask import current_app
from werkzeug.local import LocalProxy
from flask_security import roles_accepted

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)

# define a new Flask Blueprint that is register under
# the url path /file_management
blueprint = Blueprint(
    'grant_staff',
    __name__,
    url_prefix='/grant_staff',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/grant', methods=('GET', 'POST'))
@login_required
@roles_accepted('admin', 'staff')
def grant():
    """The grant view."""
    form = StaffForm()

    # if the form is submitted and valid
    if form.validate_on_submit():
        # store the form information and define the role to grant
        user = form.email.data
        role = "staff"

        user, role = _datastore._prepare_role_modify_args(user, role)

        # check if the user exist
        if user is None:
            return redirect(url_for('grant_staff.user_not_found'))
        # if successfull print it in the terminal with green color
        if _datastore.add_role_to_user(user, role):
            print('\x1b[0;32;40m' + 'Role "' + str(role) + '" added '
                  'to user "' + str(user) + '" successfully.' + '\x1b[0m')
        else:
            # Cannot add role to user
            return redirect(url_for('grant_staff.cannot_add_role'))
        # commit the changes to the database
        _datastore.commit()

        # redirect to the success page
        return redirect(url_for('grant_staff.success'))
    return render_template('grant_staff/grant.html', form=form)


@blueprint.route("/success")
@login_required
def success():
    """The success view."""
    return render_template('grant_staff/success.html')


@blueprint.route("/cannot_add_role")
@login_required
def cannot_add_role():
    """The cannot add role view."""
    return render_template('grant_staff/cannot_add_role.html'), 409


@blueprint.route("/user_not_found")
@login_required
def user_not_found():
    """The user not found view."""
    return render_template('grant_staff/user_not_found.html'), 404
