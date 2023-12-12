import os

from flask import current_app, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class ModelSelectionForm(FlaskForm):
    model_type = SelectField('Model Type', choices=[
        ('spacy_core', 'spaCy Core Models'),
        ('huggingface', 'Hugging Face Models'),
        ('custom', 'Custom Models')
    ], validators=[DataRequired()])
    model_name = StringField('Model Name/Path')
    submit = SubmitField('Load Model')

    spacy_model = SelectField('spaCy Model', choices=[
        ('en_core_web_sm', 'English - Small'),
        ('en_core_web_md', 'English - Medium')
        # ... other spaCy models ...
    ], validators=[DataRequired()])

    custom_model = SelectField('Custom Model', validators=[Optional()])  # Optional, as it's not always required

    def __init__(self, *args, **kwargs):
        super(ModelSelectionForm, self).__init__(*args, **kwargs)
        self.populate_custom_models()

    def populate_custom_models(self):
        models_dir = current_app.config['MODEL_DIR']
        if os.path.exists(models_dir):
            # List directories only, as each model is in its own folder
            model_names = [name for name in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, name))]
            self.custom_model.choices = [(model, model) for model in model_names]
        else:
            self.custom_model.choices = []
            flash("Model directory not found.", "error")


class ModelSaveForm(FlaskForm):
    custom_model_name = StringField('Custom Model Name', validators=[DataRequired()])
    save = SubmitField('Save Model')
