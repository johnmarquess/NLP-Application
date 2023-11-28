from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired


class FileUploadForm(FlaskForm):
    file = FileField('Choose File', validators=[
        DataRequired(message='No file selected!'),
        FileAllowed(['xls', 'xlsx'], 'Only .xls and .xlsx files can be uploaded here!')
    ])
    submit = SubmitField('Upload')


class WorksheetSelectionForm(FlaskForm):
    worksheet = SelectField('Select Worksheet', choices=[])
    submit = SubmitField('View Columns')


class SpacyModelForm(FlaskForm):
    model = RadioField('Model', choices=[
        ('en-core-web-sm', 'en-core-web-sm'),
        ('en-core-web-md', 'en-core-web-md'),
        ('en-core-web-lg', 'en-core-web-lg'),
        ('en-blank', 'en-blank')
    ])
    submit = SubmitField('Load Model')
