"""Views for grant_roles permission to other users."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for
from flask_babelex import gettext as _
from flask_login import login_required
from flask_menu import register_menu
from flask_security import current_user, roles_accepted

from .api import grant_room_creator_permission, grant_staff_permission
from .forms import RolesForm

# define a new Flask Blueprint that is register under
# the url path /grant_roles
blueprint = Blueprint(
    'grant_roles',
    __name__,
    url_prefix='/grant_roles',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/grant', methods=('GET',))
@login_required
@roles_accepted('admin', 'staff')
@register_menu(blueprint, 'settings.grant',
               _('%(icon)s Concedi permessi',
                   icon='<i class="fa fa-users fa-fw"></i>'),
               order=7,
               visible_when=lambda: bool(current_user.has_role('admin') or
                                         current_user.has_role('staff')
                                         ) is not False
               )
def grant():
    """The grant view."""
    form = RolesForm()
    return render_template('grant_roles/grant.html', form=form)


@blueprint.route('/grant_staff', methods=('GET', 'POST'))
@login_required
@roles_accepted('admin', 'staff')
def grant_staff():
    """The grant staff view."""
    form = RolesForm()

    # if the form is submitted and valid
    if form.validate_on_submit():
        # store the form information
        user = form.email.data

        status = grant_staff_permission(user)

        # check if the user exist
        if status == 404:
            return redirect(url_for('grant_roles.user_not_found'))
        # if successfull print it in the terminal with green color
        if status == 409:
            # Cannot add role to user
            return redirect(url_for('grant_roles.cannot_add_role'))

        # redirect to the success page
        return redirect(url_for('grant_roles.success'))
    return redirect(url_for('grant_roles.grant'))


@blueprint.route('/grant_room_creator', methods=('GET', 'POST'))
@login_required
@roles_accepted('admin')
def grant_room_creator():
    """The grant roomCreator view."""
    form = RolesForm()

    # if the form is submitted and valid
    if form.validate_on_submit():
        # store the form information
        user = form.email.data

        status = grant_room_creator_permission(user)

        # check if the user exist
        if status == 404:
            return redirect(url_for('grant_roles.user_not_found'))
        # if successfull print it in the terminal with green color
        if status == 409:
            # Cannot add role to user
            return redirect(url_for('grant_roles.cannot_add_role'))

        # redirect to the success page
        return redirect(url_for('grant_roles.success'))
    return redirect(url_for('grant_roles.grant'))


@blueprint.route("/success")
@login_required
def success():
    """The success view."""
    return render_template('grant_roles/success.html')


@blueprint.route("/cannot_add_role")
@login_required
def cannot_add_role():
    """The cannot add role view."""
    return render_template('grant_roles/cannot_add_role.html'), 409


@blueprint.route("/user_not_found")
@login_required
def user_not_found():
    """The user not found view."""
    return render_template('grant_roles/user_not_found.html'), 404
