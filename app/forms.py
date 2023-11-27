from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class UploadForm(FlaskForm):
    file = FileField('Select a file', validators=[
        FileRequired(),
        FileAllowed(['csv', 'xls', 'xlsx', 'pkl', 'parquet'], 'Only specific file types are allowed!')
    ])
    submit = SubmitField('Upload')
