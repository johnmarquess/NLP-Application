from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, RadioField, SelectField, HiddenField
from wtforms.validators import Optional


class FileUploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Upload')


class LoadSpreadsheetForm(FlaskForm):
    selected_file = HiddenField()  # Hidden field to store the selected file name
    file_choice = RadioField('Select File', choices=[], coerce=str)
    worksheet_choice = SelectField('Select Worksheet', choices=[], coerce=str)
    submit = SubmitField('View Worksheet')


class CleanDataForm(FlaskForm):
    file_choice = RadioField('Select File', choices=[], coerce=str)
    submit = SubmitField('View File')  # No need to set 'name' here

