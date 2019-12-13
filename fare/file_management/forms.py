"""file_management form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField

from flask_wtf.file import FileField, FileRequired


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
    school_order = StringField(
        'School order', [validators.DataRequired()]
    )
    discipline = StringField(
        'Discipline', [validators.DataRequired()]
    )
    argument = StringField(
        'Argument', [validators.DataRequired()]
    )
    description = TextAreaField(
        'Description', [validators.DataRequired()]
    )


class DeleteForm(FlaskForm):
    """ form to delete files """

    file_bucket = StringField('Id of the bucket', [validators.DataRequired()])
