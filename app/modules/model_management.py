import spacy
from flask import flash, session


class ModelManager:
    def __init__(self):
        self.nlp = None

    def load_spacy_model_from_session(self):
        model_choice = session.get('selected_model', 'en_core_web_sm')
        if model_choice:
            try:
                if model_choice in ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']:
                    self.nlp = spacy.load(model_choice)
                else:
                    flash(f"Invalid model choice: {model_choice}", 'danger')
                    return None
            except Exception as e:
                flash(f"Failed to load model {model_choice}: {str(e)}", 'danger')

    # Additional methods like save_model, update_model, etc.

    @property
    def model(self):
        return self.nlp

    @staticmethod
    def set_model_in_session(model_name):
        session['selected_model'] = model_name

    @staticmethod
    def get_model_from_session():
        return session.get('selected_model')
