import os

from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from app import app


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file_post():
    if 'datafile' not in request.files:
        return redirect(request.url)
    file = request.files['datafile']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('index'))
