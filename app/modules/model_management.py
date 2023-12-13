import os

import spacy
from flask import current_app, session
from transformers import AutoModel, AutoTokenizer


class ModelManager:
    def __init__(self, model_name=None):
        self.model_name = model_name
        self.nlp = None
        if model_name:
            self.load_model(model_name)

    def load_model(self, model_type, model_identifier):
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

            elif model_type == 'huggingface':
                # Set up the Hugging Face access token
                os.environ["HF_ACCESS_TOKEN"] = current_app.config['HF_ACCESS_TOKEN']
                model = AutoModel.from_pretrained(model_identifier)
                tokenizer = AutoTokenizer.from_pretrained(model_identifier)
                # Here you can handle the loaded model and tokenizer
                return f"Hugging Face model {model_identifier} loaded successfully", (model, tokenizer)

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
