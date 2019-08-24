"""file_management form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from wtforms import StringField, validators


class RecordForm(FlaskForm):
    """file_management form."""

    title = StringField(
        'Title', [validators.DataRequired()]
    )
    contributor_name = StringField(
        'Name of the contributor', [validators.DataRequired()]
    )
