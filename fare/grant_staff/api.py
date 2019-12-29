from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


def grant_staff_permission(user):
    """ Grant staff permission to  a user
        param string user: the email of the user that obtain staff permission
    """
    role = "staff"

    user, role = _datastore._prepare_role_modify_args(user, role)

    # check if the user exist
    if user is None:
        return 404
    # if successfull print it in the terminal with green color
    if _datastore.add_role_to_user(user, role):
        print('\x1b[0;32;40m' + 'Role "' + str(role) + '" added '
              'to user "' + str(user) + '" successfully.' + '\x1b[0m')
    else:
        # Cannot add role to user
        return 409
    # commit the changes to the database
    _datastore.commit()

    return 200
