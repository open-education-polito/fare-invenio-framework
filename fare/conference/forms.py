"""conference form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, validators


class RoomForm(FlaskForm):
    """conference form."""

    roomId = StringField(
        'Room id', [validators.DataRequired(),
                    validators.Regexp(r'^[\w.@+-]+$', message="Il campo non può contenere spazi")]
    )

    password = PasswordField(
        'Room password', [validators.DataRequired()]
    )

    username = StringField(
        'Name of the user', [validators.DataRequired()]
    )
