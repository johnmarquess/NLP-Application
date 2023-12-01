import os

import pandas as pd
from flask import current_app, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import RadioField, SelectField, SubmitField, HiddenField, BooleanField
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
    selected_worksheet = SelectField('Select Worksheet', choices=[])
    selected_file = HiddenField()  # Hidden field to store selected file name
    submit = SubmitField('View Columns')


class SpacyModelForm(FlaskForm):
    model = RadioField('Model', choices=[
        ('en_core_web_sm', 'English - Small'),
        ('en_core_web_md', 'English - Medium'),
        ('en_core_web_lg', 'English - Large'),
        ('en', 'English - Blank'),
    ])
    submit = SubmitField('Submit')


class PreprocessingForm(FlaskForm):
    # Dropdown for selecting the file
    file = SelectField(label='Select a CSV file from your list of saved files.', validators=[DataRequired()])
    # Checkbox fields for preprocessing options
    lemmatize = BooleanField('Lemmatize')
    remove_stopwords = BooleanField('Remove English Stop Words')
    remove_punctuation = BooleanField('Remove Punctuation')
    remove_spaces = BooleanField('Remove Spaces')
    remove_special_chars = BooleanField('Remove Special Characters')
    remove_newlines = BooleanField('Remove Newline Characters')
    lowercase = BooleanField('Make Lowercase')
    # # Field for renaming the data column
    column_to_preprocess = SelectField('Select column to preprocess', choices=[], validators=[DataRequired()])
    # Options for storing the preprocessed data
    store_as = SelectField('Store As', choices=[('string', 'String'), ('tokens', 'List of Tokens')])
    submit = SubmitField('Process')

    def __init__(self, *args, **kwargs):
        super(PreprocessingForm, self).__init__(*args, **kwargs)
        self.column_to_preprocess.choices = [('default', 'Please Select a File First')]
        self.populate_file_choices()

    def populate_file_choices(self):
        # Constructing an absolute path to the 'data_saved' directory
        saved_files_path = os.path.join(current_app.root_path, current_app.config['DATA_SAVED'])

        # Check if directory exists
        if os.path.exists(saved_files_path):
            saved_files = [f for f in os.listdir(saved_files_path) if f.endswith('.csv')]
            self.file.choices = [(f, f) for f in saved_files]
        else:
            # Handle the case where the directory does not exist
            self.file.choices = []
            flash("Data saved directory not found.", "error")

    def populate_column_choices(self, file_path):
        """ Populate the column_to_preprocess field with column names from the CSV file. """
        try:
            df = pd.read_csv(file_path)
            self.column_to_preprocess.choices = [(col, col) for col in df.columns]
        except Exception as e:
            self.column_to_preprocess.choices = []
            flash(f"Error reading file: {e}", "error")
