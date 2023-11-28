import os

from flask import current_app

from app.forms import FileUploadForm, RawFileSelectionForm, SavedFileSelectionForm


def get_saved_files():
    data_saved_path = os.path.join(current_app.root_path, current_app.config['DATA_SAVED'])
    return os.listdir(data_saved_path)


def prepare_file_management_forms():
    form = FileUploadForm()
    raw_file_form = RawFileSelectionForm()
    saved_file_form = SavedFileSelectionForm()

    raw_files = os.listdir(os.path.join('app', current_app.config['DATA_RAW']))
    saved_files = os.listdir(os.path.join('app', current_app.config['DATA_SAVED']))

    raw_file_form.selected_file.choices = [(file, file) for file in raw_files]
    saved_file_form.selected_saved_file.choices = [(file, file) for file in saved_files]

    return form, raw_file_form, saved_file_form, raw_files, saved_files