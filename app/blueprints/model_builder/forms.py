from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired


class ModelSelectionForm(FlaskForm):
    model_type = RadioField('Model Type', choices=[
        ('topic_modelling', 'Topic Modelling'),
        ('classification', 'Classification'),
        ('ner', 'Named Entity Recognition'),
        ('update_ner', 'Update NER model')
        # Add more choices as needed
    ])
    submit = SubmitField('Select')


class ModelDataSelectionForm(FlaskForm):
    file = SelectField('Select File', validators=[DataRequired()])
    column = SelectField('Select Column')
    all_columns = BooleanField('Select All Columns')
    submit = SubmitField('Submit')
