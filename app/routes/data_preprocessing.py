import os
import re

import pandas as pd
import spacy
from flask import Blueprint, render_template, flash, session, request, jsonify, current_app

from app.forms import SpacyModelForm, PreprocessingForm
from app.utils import get_file_path

data_preprocessing_bp = Blueprint('data_preprocessing', __name__)


def load_spacy_model_from_session():
    """
    Load Spacy Model from Session

    Loads a Spacy model based on the selected model choice stored in the session.

    :return: A Spacy language model object or None if there was an error.
    """
    model_choice = session.get('selected_model')
    if model_choice:
        try:
            # Check if the model choice is one of the English models
            if model_choice in ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']:
                nlp = spacy.load(model_choice)
            elif model_choice == 'en':
                # Load a blank English model
                nlp = spacy.blank('en')
            else:
                flash(f"Invalid model choice: {model_choice}", 'danger')
                return None

            return nlp
        except Exception as e:
            flash(f"Failed to load model {model_choice}: {str(e)}", 'danger')

    return None


# Function to preprocess each text entry
def preprocess_text(text, nlp, lemmatize=False, remove_stopwords=False, remove_punct=False, remove_spaces=False,
                    remove_special_chars=False, remove_newlines=False, lowercase=False, store_as='string'):
    """
    :param text: The text to be preprocessed
    :param nlp: The pre-trained spaCy model to be used for text processing
    :param lemmatize: Whether to lemmatize the tokens. Defaults to False.
    :param remove_stopwords: Whether to remove stopwords from the text. Defaults to False.
    :param remove_punct: Whether to remove punctuation from the text. Defaults to False.
    :param remove_spaces: Whether to remove spaces from the text. Defaults to False.
    :param remove_special_chars: Whether to remove special characters from the text. Defaults to False.
    :param remove_newlines: Whether to remove newline characters from the text. Defaults to False.
    :param lowercase: Whether to convert the text to lowercase. Defaults to False.
    :param store_as: The format to store the processed text. Defaults to 'string'. Choose between 'string' or 'tokens'.
    :return: The preprocessed text or tokens, depending on the value of store_as parameter.

    """
    if pd.isna(text):
        return ''
    text = str(text)
    if remove_newlines:
        text = text.replace('\n', '')
    if remove_special_chars:
        text = re.sub(r'[^A-Za-z0-9 ]', ' ', text)  # Added space in regex to keep spaces
    if lowercase:
        text = text.lower()

    doc = nlp(text)
    processed_tokens = []

    for token in doc:
        if remove_stopwords and token.is_stop:
            continue
        if remove_punct and token.is_punct:
            continue
        if remove_spaces and token.is_space:
            continue

        token_text = token.lemma_ if lemmatize else token.text
        processed_tokens.append(token_text)

    if store_as == 'tokens':
        return processed_tokens
    else:
        return ' '.join(processed_tokens)


@data_preprocessing_bp.route('/get-columns')
def get_columns():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "No file name provided"}), 400

    file_path = get_file_path(file_name)
    df = pd.read_csv(file_path)
    columns = df.columns.tolist()
    return jsonify(columns=columns)


@data_preprocessing_bp.route('/data_preprocessing', methods=['GET', 'POST'])
def data_preprocessing():
    """
    Preprocesses data using spaCy models and various options.
    This route handles the following:
    1. Load a spaCy model
    2. Select a file to preprocess
    3. Select a column to preprocess
    4. Select preprocessing options
    5. Preprocess the selected column
    6. Save the processed data as a CSV file

    :return: None

    """
    spacy_model_form = SpacyModelForm()
    preprocessing_form = PreprocessingForm()
    processed_data_head = None
    summary = {}

    # Handle spaCy model form submission
    if spacy_model_form.validate_on_submit():
        model_choice = spacy_model_form.model.data
        session['selected_model'] = model_choice
        flash(f'Model {model_choice} loaded successfully!', 'success')

        # Populate column choices when a file is selected
    if preprocessing_form.file.data:
        file_path = get_file_path(preprocessing_form.file.data)
        preprocessing_form.populate_column_choices(file_path)

    if preprocessing_form.validate_on_submit():
        # Load spaCy model from session
        nlp = load_spacy_model_from_session()
        if nlp:
            file_path = get_file_path(preprocessing_form.file.data)
            df = pd.read_csv(file_path)
            summary['Model'] = nlp.meta['name']  # Add model name to summary
            summary['Processed File'] = preprocessing_form.file.data  # Add file to summary
            summary['Selected Column'] = preprocessing_form.column_to_preprocess.data  # Add column to summary

            # Get the selected column
            selected_column = preprocessing_form.column_to_preprocess.data
            store_as = preprocessing_form.store_as.data
            # Apply preprocessing to the selected column
            df['processed_text'] = df[selected_column].apply(lambda x: preprocess_text(
                x,
                nlp,  # Loaded spaCy model
                lemmatize=preprocessing_form.lemmatize.data,
                lowercase=preprocessing_form.lowercase.data,
                remove_stopwords=preprocessing_form.remove_stopwords.data,
                remove_punct=preprocessing_form.remove_punctuation.data,
                remove_spaces=preprocessing_form.remove_spaces.data,
                remove_special_chars=preprocessing_form.remove_special_chars.data,
                remove_newlines=preprocessing_form.remove_newlines.data,
                store_as=store_as
            ))
            processed_data_head = df.head().to_html(classes='table table-striped', header=True,
                                                    index=False)

            processed_data_head = df.head().to_html(classes='table table-striped', header=True, index=False)
            summary['Number of Rows'] = df.shape[0]  # Add number of rows to summary
            summary['Preprocessing Options'] = ', '.join(
                opt for opt in
                ['lemmatize', 'lowercase', 'remove_stopwords', 'remove_punctuation', 'remove_special_chars',
                 'remove_spaces', 'remove_newlines', ]
                if preprocessing_form[opt].data
            )

            if preprocessing_form.output_filename.data:
                output_file = preprocessing_form.output_filename.data
                # Append '.csv' if not already present
                if not output_file.lower().endswith('.csv'):
                    output_file += '.csv'

                output_path = os.path.join(current_app.root_path, current_app.config['DATA_PROCESSED'], output_file)

                # Check if file already exists and avoid overwriting
                if os.path.exists(output_path):
                    flash(f"File {output_file} already exists. Please choose a different name.", "warning")
                else:
                    try:
                        df.to_csv(output_path, index=False)
                        flash(f"Processed data saved as {output_file} in data_processed folder.", "success")
                    except Exception as e:
                        flash(f"Failed to save file: {e}", "error")

    return render_template('data_preprocessing.html', spacy_model_form=spacy_model_form,
                           preprocessing_form=preprocessing_form, processed_data_head=processed_data_head,
                           summary=summary)
