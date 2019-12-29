"""Views for grant_staff permission to other users."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from .forms import StaffForm
from .api import grant_staff_permission
from flask_security import roles_accepted


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
        # store the form information
        user = form.email.data

        status = grant_staff_permission(user)

        # check if the user exist
        if status == 404:
            return redirect(url_for('grant_staff.user_not_found'))
        # if successfull print it in the terminal with green color
        if status == 409:
            # Cannot add role to user
            return redirect(url_for('grant_staff.cannot_add_role'))

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
