import re

import pandas as pd


class NLPProcessor:
    def __init__(self, nlp):
        # Load the specified spaCy model
        self.nlp = nlp

    def preprocess_text(self, text, options):
        if pd.isna(text):
            return ''
        text = str(text)
        if options.get('remove_newlines', False):
            text = text.replace('\n', '')
        if options.get('remove_special_chars', False):
            text = re.sub(r'[^A-Za-z0-9 ]|\b[a-zA-Z]\b', ' ', text)  # Keep spaces
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
