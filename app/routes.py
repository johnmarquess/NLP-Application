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


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'datafile' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['datafile']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Change this to save in the DATA_RAW_FOLDER
            file.save(os.path.join(app.config['DATA_RAW_FOLDER'], filename))
            flash(f'File uploaded successfully to {app.config["DATA_RAW_FOLDER"]}', 'success')
            return redirect(url_for('index'))  # Or any other route you'd like to redirect to
    return render_template('upload.html')


@app.route('/data_management')
def data_management():
    files = os.listdir(app.config['DATA_RAW_FOLDER'])
    return render_template('data_management.html', files=files)


@app.route('/data_modeling')
def data_modeling():
    return render_template('data_modeling.html')
