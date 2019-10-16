"""grant_staff form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.html5 import EmailField


class StaffForm(FlaskForm):
    """grant_staff form."""

    email = EmailField(
        'Email', [validators.DataRequired(), validators.Email()]
    )
