from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


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


class TopicModellingForm(FlaskForm):
    tfidf_transform = BooleanField("TF-IDF Transformation")
    num_topics = StringField("Number of Topics", validators=[DataRequired()])
    random_state = StringField("Random State", validators=[DataRequired()])
    chunksize = StringField("Chunk Size", validators=[DataRequired()])
    passes = StringField("Number of Passes", validators=[DataRequired()])
    per_word_topics = BooleanField("Per Word Topics")
    visualization_name = StringField("Visualization Name", validators=[DataRequired()])
    submit = SubmitField("Build Topic Model")

    def validate_num_topics(self, field):
        field.data = int(field.data)
        # Assuming 'num_topics' is the field name
        if field.data < 1 or field.data > 15:
            raise ValidationError('Number of topics must be between 1 and 15.')

    def validate_random_state(self, field):
        # Assuming 'random_state' is the field name
        field.data = int(field.data)
        if field.data < 1 or field.data > 5000:
            raise ValidationError('Random state must be between 1 and 5000.')

    def validate_chunksize(self, field):
        # Assuming 'chunksize' is the field name
        field.data = int(field.data)
        if field.data < 1 or field.data > 10:
            raise ValidationError('Chunk size must be between 1 and 10.')

    def validate_passes(self, field):
        # Assuming 'passes' is the field name
        field.data = int(field.data)
        if field.data < 5 or field.data > 50:
            raise ValidationError('Number of passes must be between 5 and 50.')

    # Add similar validators for random_state, chunksize, and passes
