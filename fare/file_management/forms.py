"""file_management form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from .utils import read_menu_fields
from wtforms import IntegerField, StringField, TextAreaField, validators, SelectField


class RecordForm(FlaskForm):
    """file_management form."""

    file_content = FileField(
        'File of the record', validators=[FileRequired()]
    )
    title = StringField(
        'Title', [validators.DataRequired()]
    )
    contributor_name = StringField(
        'Name of the contributor', [validators.DataRequired()]
    )
    educationLevel = SelectField(
        'Education level', choices=read_menu_fields("educationLevel")
    )
    subject = SelectField(
        'Subject', choices=read_menu_fields("subject")
    )
    coverage = StringField(
        'Coverage', [validators.DataRequired()]
    )
    description = TextAreaField(
        'Description', [validators.DataRequired()]
    )


class UtilsForm(FlaskForm):
    """form to delete, download and publish files."""

    file_bucket = StringField('Id of the bucket', [validators.DataRequired()])
    record_id = IntegerField('Id of the record', [validators.DataRequired()])
