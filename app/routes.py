import os

from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .forms import UploadForm
from .utils.file_handling import list_files

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/data-management', methods=['GET', 'POST'])
def data_management():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        save_path = os.path.join('data/data_raw', filename)

        try:
            file.save(save_path)
            flash(f'File {filename} has been successfully saved.', 'success')
        except Exception as e:
            flash(f'An error occurred while saving the file: {e}', 'danger')

        return redirect(url_for('main.data_management'))

    raw_files = list_files('data/data_raw')
    saved_files = list_files('data/data_saved')

    return render_template('data_management.html', form=form, raw_files=raw_files, saved_files=saved_files)


@main.route('/data-modeling')
def data_modeling():
    return render_template('data_modeling.html')  # Assumes you have a template for this


@main.route('/reporting')
def reporting():
    return render_template('reporting.html')  # Assumes you have a template for this
