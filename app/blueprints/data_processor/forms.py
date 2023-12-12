import os

import pandas as pd
from flask import current_app, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired


class DataProcessingForm(FlaskForm):
    # Dropdown for selecting the file
    file = SelectField(label='Choose a CSV file from your list of saved files.', validators=[DataRequired()])
    # Checkbox fields for preprocessing options
    lemmatize = BooleanField('Lemmatize')
    remove_stopwords = BooleanField('Remove English Stop Words')
    remove_punctuation = BooleanField('Remove Punctuation')
    remove_spaces = BooleanField('Remove Spaces')
    remove_special_chars = BooleanField('Remove Special Characters')
    remove_newlines = BooleanField('Remove Newline Characters')
    lowercase = BooleanField('Make Lowercase')
    # # Field for renaming the data column
    column_to_preprocess = SelectField('Choose column to preprocess', choices=[], validators=[DataRequired()])
    # Options for storing the preprocessed data
    store_as = SelectField('Store As', choices=[('string', 'String'), ('tokens', 'List of Tokens')])
    submit = SubmitField('Process')
    output_filename = StringField('Output Filename', validators=[DataRequired()])

    # def __init__(self, *args, **kwargs):
    #     super(DataProcessingForm, self).__init__(*args, **kwargs)
    #     self.populate_file_choices()

    def populate_file_choices(self):
        saved_files_path = os.path.join(current_app.root_path, current_app.config['CLEAN_DATA_DIR'])
        if os.path.exists(saved_files_path):
            saved_files = [f for f in os.listdir(saved_files_path) if f.endswith('.csv')]
            self.file.choices = [('', 'Select a CSV File')] + [(f, f) for f in saved_files]
        else:
            self.file.choices = [('', 'Select a CSV File')]
            flash("Data saved directory not found.", "error")

    def populate_column_choices(self, file_path):
        """ Populate the column_to_preprocess field with column names from the CSV file. """
        try:
            df = pd.read_csv(file_path)
            self.column_to_preprocess.choices = [(col, col) for col in df.columns]
        except Exception as e:
            self.column_to_preprocess.choices = []
            flash(f"Error reading file: {e}", "error")
