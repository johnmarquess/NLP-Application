import os

import pandas as pd
import spacy
from flask import Blueprint, render_template, flash, current_app, redirect, url_for, request, jsonify

from app.modules.data_processing import NLPProcessor
from app.modules.file_management import FileManagement
from .forms import DataProcessingForm

data_processor_bp = Blueprint('data_processor', __name__)


@data_processor_bp.route('/data-processing', methods=['GET', 'POST'])
def data_processing():
    file_manager = FileManagement()
    preprocess_form = DataProcessingForm()
    preprocess_form.populate_file_choices()
    summary = {}

    if request.method == 'POST':
        selected_file = preprocess_form.file.data
        file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], selected_file)

        if selected_file:
            preprocess_form.populate_column_choices(file_path)

        if 'process_submit' in request.form:
            if preprocess_form.validate():
                print("Form validation successful")

                try:
                    df = pd.read_csv(file_path)
                    preprocess_form.column_to_preprocess.choices = [(col, col) for col in df.columns]
                except Exception as e:
                    flash(f"Error reading file: {e}", 'error')
                    return redirect(url_for('data_processor.data_processing'))

                try:
                    nlp = spacy.load('en_core_web_sm')
                except Exception as e:
                    flash(f"Failed to load the spaCy model: {str(e)}", 'danger')
                    return redirect(url_for('data_processor.data_processing'))

                processor = NLPProcessor(nlp)
                options = {
                    'lemmatize': preprocess_form.lemmatize.data,
                    'remove_stopwords': preprocess_form.remove_stopwords.data,
                    'remove_punctuation': preprocess_form.remove_punctuation.data,
                    'remove_spaces': preprocess_form.remove_spaces.data,
                    'remove_special_chars': preprocess_form.remove_special_chars.data,
                    'remove_newlines': preprocess_form.remove_newlines.data,
                    'lowercase': preprocess_form.lowercase.data,
                    'store_as': preprocess_form.store_as.data
                }

                df['processed_data'] = df[preprocess_form.column_to_preprocess.data].apply(
                    lambda x: processor.preprocess_text(x, options)
                )

                summary['Model'] = nlp.meta['name']
                summary['Processed File'] = preprocess_form.file.data
                summary['Processed Column'] = preprocess_form.column_to_preprocess.data
                summary['Number of Rows'] = df.shape[0]
                summary['Preprocessing Options'] = ', '.join(
                    opt for opt in
                    ['lemmatize', 'lowercase', 'remove_stopwords', 'remove_punctuation', 'remove_special_chars',
                     'remove_spaces', 'remove_newlines', ]
                    if preprocess_form[opt].data
                )

                if preprocess_form.output_filename.data:
                    output_file = preprocess_form.output_filename.data
                    if not output_file.lower().endswith('.csv'):
                        output_file += '.csv'

                    output_path = os.path.join(current_app.config['PROCESSED_DATA_DIR'], output_file)

                    if os.path.exists(output_path):
                        flash(f'File {output_file} already exists. Please choose a different name.', 'warning')
                    else:
                        try:
                            save_message = file_manager.save_as_csv(df, output_file, 'PROCESSED_DATA_DIR')
                            flash(save_message, 'success')
                        except Exception as e:
                            flash(f'Failed to save file: {e}', 'error')

            else:
                print("Form validation failed")
                print(preprocess_form.errors)
                file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], preprocess_form.file.data)

    return render_template('data_processing.html', preprocess_form=preprocess_form, summary=summary)


@data_processor_bp.route('/get-columns/<filename>')
def get_columns(filename):
    file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], filename)
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return jsonify(columns)
    except Exception as e:
        return jsonify({"error": str(e)})
