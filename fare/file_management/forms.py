"""file_management form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from .utils import read_menu_fields, init_field_all, get_all_arguments
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
    coverage = SelectField(
        'Coverage', choices=init_field_all()
    )
    description = TextAreaField(
        'Description', [validators.DataRequired()]
    )
    license = SelectField(
        'License', choices=(['CC BY', 'CC BY'],
                            ['CC BY-SA', 'CC BY-SA'],
                            ['CC BY-NC', 'CC BY-NC'],
                            ['CC BY-ND', 'CC BY-ND'],
                            ['CC BY-NC-SA', 'CC BY-NC-SA'],
                            ['CC BY-NC-ND', 'CC BY-NC-ND']
                            )
    )

    def validate(self):
        """
        Validation that verify if the argument,
        selected in the coverage field, belongs
        to the subject selected
        :return: False if the argument does not belong to the subject
                 True otherwise
        """
        if not FlaskForm.validate(self):
            return False
        all_arguments = get_all_arguments()
        if self.coverage.data in all_arguments[self.subject.data]:
            return True
        self.coverage.errors.append("Subject and argument must be compatible")
        return False


class UtilsForm(FlaskForm):
    """form to delete, download and publish files."""

    file_bucket = StringField('Id of the bucket', [validators.DataRequired()])
    record_id = IntegerField('Id of the record', [validators.DataRequired()])
