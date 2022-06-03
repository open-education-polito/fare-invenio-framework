"""api for grant_roles module."""
from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


def grant_staff_permission(user_email):
    """Grant staff permission to  a user.

    param string user_email: the email of the user that obtain staff permission
    """
    role = "staff"

    user, role = _datastore._prepare_role_modify_args(user_email, role)

    # check if the user exist
    if user is None:
        current_app.logger.error('User "' + str(user_email) +
                                 '" does not exist')
        return 404
    # if successfull print it in the terminal with green color
    if _datastore.add_role_to_user(user, role):
        current_app.logger.info('Role "' + str(role) +
                                '" added to "' + str(user) + '" successfully')
    else:
        # Cannot add role to user
        current_app.logger.error('"' + str(user) +
                                 '" has already the "' + str(role) + '" role')
        return 409
    # commit the changes to the database
    _datastore.commit()

    return 200


def grant_room_creator_permission(user_email):
    """Grant roomCreator permission to  a user.

    param string user_email: user email that obtaining roomCreator permission
    """
    role = "roomCreator"

    user, role = _datastore._prepare_role_modify_args(user_email, role)

    # check if the user exist
    if user is None:
        current_app.logger.error('User "' + str(user_email) +
                                 '" does not exist')
        return 404
    # if successfull print it in the terminal with green color
    if _datastore.add_role_to_user(user, role):
        current_app.logger.info('Role "' + str(role) +
                                '" added to "' + str(user) + '" successfully')
    else:
        # Cannot add role to user
        current_app.logger.error('"' + str(user) +
                                 '" has already the "' + str(role) + '" role')
        return 409
    # commit the changes to the database
    _datastore.commit()

    return 200
