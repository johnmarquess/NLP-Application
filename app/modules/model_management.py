import os

import pandas as pd
import spacy
from flask import current_app, session
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span


class ModelManager:
    def __init__(self, model_name=None):
        self.model_name = model_name
        self.nlp = None
        if model_name:
            self.load_model(model_name)

    @staticmethod
    def load_model(model_type, model_identifier):
        try:
            if model_type == 'spacy_core':
                nlp = spacy.load(model_identifier)
                session['spacy_model_name'] = model_identifier
                return f"spaCy model {model_identifier} loaded successfully", nlp

            elif model_type == 'custom':
                custom_model_path = os.path.join(current_app.config['MODEL_DIR'], model_identifier)
                nlp = spacy.load(custom_model_path)
                session['custom_model_name'] = model_identifier
                return f"Custom model {model_identifier} loaded successfully", nlp


        except Exception as e:
            return f"Error loading model: {str(e)}", None

    @staticmethod
    def save_model_with_custom_name(model_name, custom_name):
        try:
            nlp = spacy.load(model_name)
            model_output_dir = current_app.config['MODEL_DIR']
            custom_model_path = os.path.join(model_output_dir, custom_name)

            # Create the directory if it does not exist
            if not os.path.exists(model_output_dir):
                os.makedirs(model_output_dir)

            nlp.to_disk(custom_model_path)
            return f"Model saved successfully with the name '{custom_name}' at {custom_model_path}"
        except Exception as e:
            return f"Error saving model: {str(e)}"

    def update_model_with_entities(self, reference_file_path):
        if not self.nlp:
            raise ValueError("No model loaded to update")

        # Count entities before update
        before_count = len(self.nlp.pipe_labels.get("ner", []))

        # Read the reference file
        df = pd.read_csv(reference_file_path)
        patterns = df.values.tolist()

        # Update the model
        ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        ruler.add_patterns([{"label": label, "pattern": pattern} for pattern, label in patterns])

        # Add phrase matcher component if multi-word entities are present
        multi_word_patterns = [pattern for pattern, label in patterns if len(pattern.split()) > 1]
        if multi_word_patterns:
            phrase_matcher = PhraseMatcher(self.nlp.vocab)
            for pattern in multi_word_patterns:
                phrase_matcher.add("CUSTOM_ENTITY", [self.nlp.make_doc(pattern)])
            self.nlp.add_pipe(self.phrase_matcher_component(phrase_matcher), before="entity_ruler")

        # Count entities after update
        after_count = len(self.nlp.pipe_labels.get("ner", []))

        return before_count, after_count

    @staticmethod
    def phrase_matcher_component(phrase_matcher):
        def custom_component(doc):
            matches = phrase_matcher(doc)
            spans = []
            for match_id, start, end in matches:
                span = Span(doc, start, end, label="CUSTOM_ENTITY")
                spans.append(span)
            doc.ents = list(doc.ents) + spans
            return doc

        return custom_component
