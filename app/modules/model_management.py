import os

import spacy
from flask import session, current_app


def load_spacy_model():
    model_name = session.get('spacy_model_name')
    if model_name:
        try:
            return spacy.load(model_name)
        except Exception as e:
            print(f"Error loading spaCy model: {e}")
            return None
    return None


def use_model(text):
    nlp = load_spacy_model()
    if nlp:
        doc = nlp(text)
        # Perform operations with the spaCy Doc object
        return doc
    else:
        # Handle the case where the model is not loaded
        return None


def load_huggingface_model(model_name, api_key):
    try:
        # Setup and load the Hugging Face model
        # Example: model = transformers.pipeline('model-pipeline', model=model_name, token=api_key)
        return model_name
    except Exception as e:
        raise e  # or handle the exception as needed


def load_local_model(model_path):
    # Logic to load local model
    pass


# noinspection PyTypeChecker
def save_model(model_name):
    nlp = spacy.load(model_name)
    models_dir = current_app.config['MODEL_DIR']
    model_path = os.path.join(models_dir, model_name)

    # Create the directory if it does not exist
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    # noinspection PyTypeChecker
    nlp.to_disk(model_path)
    return f"Model saved successfully at {model_path}"
