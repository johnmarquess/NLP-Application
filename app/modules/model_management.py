import os

import pandas as pd
import spacy
from flask import current_app, session
from spacy.pipeline import EntityRuler


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

    def add_entities_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            if 'input' not in df.columns or 'entity' not in df.columns:
                return "CSV file must contain 'input' and 'entity' columns"

            entities = [(row['input'], row['entity']) for index, row in df.iterrows()]

            model_type = 'spacy_core'  # or 'custom'
            model_identifier = session.get('spacy_model_name') or session.get('custom_model_name')

            load_message, nlp = self.load_model(model_type, model_identifier)
            if nlp is None:
                return load_message

            # Create a new EntityRuler and add patterns
            ruler = EntityRuler(nlp, overwrite_ents=True)
            patterns = [{"label": ent_type, "pattern": ent_name} for ent_name, ent_type in entities]
            ruler.add_patterns(patterns)

            # Add the EntityRuler to the pipeline
            nlp.add_pipe('entity_ruler', before="ner")
            nlp.get_pipe('entity_ruler').add_patterns(patterns)

            formatted_entities = ["{} ({})".format(pattern['pattern'], pattern['label']) for pattern in patterns]
            return "Entities added: " + ", ".join(formatted_entities)

        except Exception as e:
            return f"Error processing file: {str(e)}"
