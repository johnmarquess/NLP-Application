from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField, BooleanField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, NumberRange


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


class TopicModelingForm(FlaskForm):
    tfidf_transform = BooleanField("TF-IDF Transformation")
    num_topics = IntegerField("Number of Topics", validators=[DataRequired(), NumberRange(min=1, max=15)])
    random_state = IntegerField("Random State", validators=[DataRequired()])
    chunksize = IntegerField("Chunk Size", validators=[DataRequired(), NumberRange(min=5, max=100)])
    passes = IntegerField("Number of Passes", validators=[DataRequired(), NumberRange(min=5, max=50)])
    per_word_topics = BooleanField("Per Word Topics")
    visualization_name = StringField("Visualization Name", validators=[DataRequired()])
    submit = SubmitField("Build Topic Model")
