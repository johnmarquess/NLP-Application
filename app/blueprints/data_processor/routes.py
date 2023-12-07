import os

import pandas as pd
import spacy
from flask import Blueprint, render_template, flash, current_app, redirect, url_for, session, request, jsonify

from app.modules.data_processing import NLPProcessor
from app.modules.file_management import FileManagement
from .forms import SpacyModelForm, DataProcessingForm

data_processor_bp = Blueprint('data_processor', __name__)


@data_processor_bp.route('/data-processing', methods=['GET', 'POST'])
def data_processing():
    """
    Function that handles data processing endpoint.
    - controls model selection and stores in session - calls load_spacy_model_from_session()
    - controls data processing options
    - handles files saving - calls save_as_csv()
    - handles file viewing - calls view_csv_contents()
    - produces summary of model / data features

    Returns: rendered template with model selection form, data processing form, summary and table HTML
    """
    file_manager = FileManagement()
    model_form = SpacyModelForm()
    preprocess_form = DataProcessingForm()
    preprocess_form.populate_file_choices()
    summary = {}

    if 'model_submit' in request.form and model_form.validate_on_submit():
        session['selected_model'] = model_form.model.data
        flash("Model selected: " + model_form.model.data, 'info')
        return redirect(url_for('data_processor.data_processing'))

    if 'process_submit' in request.form:
        file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], preprocess_form.file.data)
        try:
            df = pd.read_csv(file_path)
            preprocess_form.column_to_preprocess.choices = [(col, col) for col in df.columns]
        except Exception as e:
            flash(str(e), 'error')
            return redirect(url_for('data_processor.data_processing'))

        if preprocess_form.validate_on_submit():
            nlp = NLPProcessor.load_spacy_model_from_session()

            if not nlp:
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
            summary['Number of Rows'] = df.shape[0]  # Add number of rows to summary
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
                    print(f"File exists: {output_path}")
                    flash(f'File {output_file} already exists. Please choose a different name.', 'warning')
                else:
                    try:
                        print(f"About to save file at: {output_path}")

                        save_message = file_manager.save_as_csv(df, output_file, 'PROCESSED_DATA_DIR')
                        print(f"Save message: {save_message}")
                        flash(save_message, 'success')
                        # Generate table HTML from the saved file

                    except Exception as e:
                        flash(f'Failed to save file: {e}', 'error')
                    print(f"File does not exist: {output_path}")
    return render_template('data_processing.html', model_form=model_form,
                           preprocess_form=preprocess_form, summary=summary)


@data_processor_bp.route('/load-model', methods=['POST'])
def load_model():
    data = request.get_json()
    model_choice = data.get('model')

    try:
        if model_choice in ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']:
            nlp = spacy.load(model_choice)
        # elif model_choice == 'en':
        #     nlp = spacy.blank('en')
        else:
            return jsonify({'status': 'error', 'message': f"Invalid model choice: {model_choice}"}), 400

        session['selected_model'] = model_choice
        return jsonify({'status': 'success', 'message': f"Model {model_choice} loaded successfully."})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Failed to load model {model_choice}: {str(e)}"}), 500


@data_processor_bp.route('/get-columns/<filename>')
def get_columns(filename):
    file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], filename)
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return jsonify(columns)
    except Exception as e:
        return jsonify({"error": str(e)})
