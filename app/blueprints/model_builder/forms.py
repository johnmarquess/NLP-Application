from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired


class ModelSelectionForm(FlaskForm):
    model_type = RadioField('Choose Modelling Approach', choices=[
        ('topic_modelling', 'Topic Modelling'),
        ('classification', 'Classification'),
        ('ner', 'Named Entity Recognition'),
        ('update_ner_model', 'Update NER Model')
    ])
    submit = SubmitField('Select')


class ModelDataSelectionForm(FlaskForm):
    file = SelectField('Select File', validators=[DataRequired()])
    column = SelectField('Select Column', validators=[DataRequired()], default='processed_data')
