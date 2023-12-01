import re

import pandas as pd
import spacy
from flask import Blueprint, render_template, flash, session, request, jsonify
from spacy.lang.en.stop_words import STOP_WORDS

from app.forms import SpacyModelForm, PreprocessingForm
from app.utils import get_file_path

data_modeling_bp = Blueprint('data_modeling', __name__)


def load_spacy_model_from_session():
    model_choice = session.get('selected_model')
    if model_choice:
        try:
            nlp = spacy.load(model_choice)
            return nlp
        except Exception as e:
            flash(f"Failed to load model {model_choice}: {str(e)}", 'danger')
    return None


# Function to preprocess each text entry
def preprocess_text(text, nlp, lemmatize=False, remove_stopwords=False, remove_punct=False, remove_spaces=False,
                    remove_special_chars=False, remove_newlines=False, lowercase=False, store_as='string'):
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


@data_modeling_bp.route('/get-columns')
def get_columns():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "No file name provided"}), 400

    file_path = get_file_path(file_name)
    df = pd.read_csv(file_path)
    columns = df.columns.tolist()
    return jsonify(columns=columns)


@data_modeling_bp.route('/data-modeling', methods=['GET', 'POST'])
def data_modeling():
    spacy_model_form = SpacyModelForm()
    preprocessing_form = PreprocessingForm()
    processed_data_head = None

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
            processed_data_head = df.head().to_html(classes='table table-striped', header="true",
                                                    index=False)

            # Further processing or saving the preprocessed data
            # ...

    return render_template('data_modeling.html', spacy_model_form=spacy_model_form,
                           preprocessing_form=preprocessing_form, processed_data_head=processed_data_head)
