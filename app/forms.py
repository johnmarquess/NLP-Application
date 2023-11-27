from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class FileUploadForm(FlaskForm):
    file = FileField('Choose File', validators=[
        FileAllowed(['csv', 'xls', 'xlsx', 'pickle', 'parquet'], 'Only specific file types allowed!')
    ])
    submit = SubmitField('Upload')
