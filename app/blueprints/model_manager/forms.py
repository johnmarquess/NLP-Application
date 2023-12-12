from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class ModelSelectionForm(FlaskForm):
    model_type = SelectField('Model Type', choices=[
        ('spacy_core', 'spaCy Core Models'),
        ('huggingface', 'Hugging Face Models'),
        ('local', 'Local Models')
    ], validators=[DataRequired()])
    model_name = StringField('Model Name/Path')
    submit = SubmitField('Load Model')

    spacy_model = SelectField('spaCy Model', choices=[
        ('en_core_web_sm', 'English - Small'),
        ('en_core_web_md', 'English - Medium')
        # ... other spaCy models ...
    ], validators=[DataRequired()])


class ModelSaveForm(FlaskForm):
    custom_model_name = StringField('Custom Model Name', validators=[DataRequired()])
    save = SubmitField('Save Model')
