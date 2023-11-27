from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.forms import FileUploadForm
import os


def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/data-management', methods=['GET', 'POST'])
    def data_management():
        form = FileUploadForm()
        raw_files = os.listdir(os.path.join('app', app.config['DATA_RAW']))
        saved_files = os.listdir(os.path.join('app', app.config['DATA_SAVED']))
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)

            # Prepend 'app/' to the DATA_RAW path
            save_path = os.path.join('app', app.config['DATA_RAW'])

            try:
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                f.save(os.path.join(save_path, filename))
                flash(f'File {filename} has been saved successfully!', 'success')
            except Exception as e:
                flash(f'Error saving file: {e}', 'warning')

            return redirect(url_for('data_management'))

        return render_template('data_management.html', form=form, raw_files=raw_files, saved_files=saved_files)

    @app.route('/data-modeling')
    def data_modeling():
        return render_template('data_modeling.html')

    @app.route('/reporting')
    def reporting():
        return render_template('reporting.html')
