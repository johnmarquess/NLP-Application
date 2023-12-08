from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, NumberRange


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
    no_below = IntegerField("No Below", validators=[DataRequired(), NumberRange(min=1)], default=5)
    no_above = FloatField("No Above", validators=[DataRequired(), NumberRange(min=0, max=1)], default=0.5)
    keep_n = IntegerField("Keep N", validators=[DataRequired()], default=100000)

    def validate_num_topics(form, field):
        try:
            field.data = int(field.data)
            if field.data < 1 or field.data > 15:
                raise ValidationError('Number of topics must be between 1 and 15.')
        except ValueError:
            raise ValidationError("Number of topics must be an integer.")

    def validate_random_state(form, field):
        try:
            field.data = int(field.data)
            if field.data < 1 or field.data > 5000:
                raise ValidationError('Random state must be between 1 and 5000.')
        except ValueError:
            raise ValidationError("Random state must be an integer between 1 and 5000.")

    def validate_chunksize(form, field):
        try:
            field.data = int(field.data)
            if field.data < 1 or field.data > 10:
                raise ValidationError('Chunk size must be between 1 and 10.')
        except ValueError:
            raise ValidationError("Chunk size must be an integer between 1 and 10.")

    def validate_passes(form, field):
        try:
            field.data = int(field.data)
            if field.data < 5 or field.data > 50:
                raise ValidationError('Number of passes must be between 5 and 50.')
        except ValueError:
            raise ValidationError("Number of passes must be an integer between 5 and 50.")

    def validate_no_below(self, field):
        try:
            # Assuming 'no_below' is the field name
            field.data = int(field.data)
            if field.data < 1 or field.data > 10:
                raise ValidationError('Number below must be between 1 and 10.')
        except ValueError:
            raise ValidationError("Number below must be an integer between 1 and 10.")

    def validate_no_above(self, field):
        try:
            # Assuming 'no_above' is the field name
            field.data = float(field.data)
            if field.data < 0. or field.data > 1.:
                raise ValidationError('Proportion above must be between 0 and 1.')
        except ValueError:
            raise ValidationError("Proportion above must be a float between 0 and 1.")

    def validate_keep_n(self, field):
        try:
            # Assuming 'keep_n' is the field name
            field.data = int(field.data)
            if field.data < 1 or field.data > 1000000:
                raise ValidationError('Number of words to keep must be between 1 and 1000000.')
        except ValueError:
            raise ValidationError("Number of words to keep must be an integer between 1 and 1000000.")

    submit = SubmitField("Build Topic Model")
