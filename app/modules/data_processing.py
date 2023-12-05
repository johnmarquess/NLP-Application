import re

import pandas as pd
import spacy
from flask import flash, session,jsonify


class NLPProcessor:
    def __init__(self, nlp):
        # Load the specified spaCy model
        self.nlp = nlp

    @staticmethod
    def load_spacy_model_from_session():
        """
        Load spaCy model from session.
        """
        model_choice = session.get('selected_model')
        if model_choice:
            try:
                if model_choice in ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']:
                    nlp = spacy.load(model_choice)
                # elif model_choice == 'en':
                #     nlp = spacy.blank('en')
                else:
                    flash(f"Invalid model choice: {model_choice}", 'danger')
                    return None

                return nlp
            except Exception as e:
                flash(f"Failed to load model {model_choice}: {str(e)}", 'danger')

    def preprocess_text(self, text, options):
        if pd.isna(text):
            return ''
        text = str(text)
        if options.get('remove_newlines', False):
            text = text.replace('\n', '')
        if options.get('remove_special_chars', False):
            text = re.sub(r'[^A-Za-z0-9 ]|\b[a-zA-Z]\b', ' ', text)  # Added space in regex to keep spaces
        if options.get('lowercase', False):
            text = text.lower()

        doc = self.nlp(text)
        processed_tokens = []

        for token in doc:
            if options.get('remove_stopwords', False) and token.is_stop:
                continue
            if options.get('remove_punctuation', False) and token.is_punct:
                continue
            if options.get('remove_spaces', False) and token.is_space:
                continue

            token_text = token.lemma_ if options.get('lemmatize', False) else token.text
            processed_tokens.append(token_text)

        return processed_tokens if options.get('store_as') == 'tokens' else ' '.join(processed_tokens)
