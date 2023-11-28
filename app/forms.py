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


class RawFileSelectionForm(FlaskForm):
    selected_file = RadioField('Select File', choices=[])


class SavedFileSelectionForm(FlaskForm):
    selected_saved_file = RadioField('Select Saved File', choices=[])


class WorksheetSelectionForm(FlaskForm):
    selected_sheet = SelectField('Select Worksheet', choices=[])



class SpacyModelForm(FlaskForm):
    model = RadioField('Model', choices=[
        ('en_core_web_sm', 'English - Small'),
        ('en_core_web_md', 'English - Medium'),
        ('en_core_web_lg', 'English - Large'),
        ('en', 'English - Blank'),
    ])
    submit = SubmitField('Submit')
