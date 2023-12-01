import os

import pandas as pd
from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from app.forms import WorksheetSelectionForm
from app.utils import prepare_file_management_forms

file_handling_bp = Blueprint('file_handling', __name__)


@file_handling_bp.route('/select-file', methods=['GET', 'POST'])
def select_file():
    """
    Selects a file and prepares the worksheet selection form.

    :return: Returns the rendered data_management.html template with the necessary forms and data.
    """
    form, raw_file_form, saved_file_form, raw_files, saved_files = prepare_file_management_forms()
    worksheet_selection_form = WorksheetSelectionForm()
    if raw_file_form.validate_on_submit():
        selected_file = raw_file_form.selected_file.data
        file_path = os.path.join('app', current_app.config['DATA_RAW'], selected_file)

        xls = pd.ExcelFile(file_path)
        sheets = xls.sheet_names
        worksheet_selection_form.selected_worksheet.choices = [(sheet, sheet) for sheet in sheets]

        return render_template('data_management.html', form=form, raw_file_form=raw_file_form,
                               saved_file_form=saved_file_form, worksheets=sheets, selected_file=selected_file,
                               worksheet_selection_form=worksheet_selection_form)  # Pass the form here

    return redirect(url_for('data_management.data_management'))


@file_handling_bp.route('/save-csv', methods=['POST'])
def save_csv():
    """
    Save the selected worksheet as a CSV file.

    :return: None
    """
    selected_file = request.form['selected_file']
    selected_sheet = request.form['selected_sheet']
    selected_columns = request.form.getlist('selected_columns')
    csv_name = request.form['csv_name'] + '.csv'
    file_path = os.path.join('app', current_app.config['DATA_RAW'], selected_file)
    save_path = os.path.join('app', current_app.config['DATA_SAVED'], csv_name)

    try:
        # Read the selected worksheet
        df = pd.read_excel(file_path, sheet_name=selected_sheet)

        # Select the specified columns
        df_selected = df[selected_columns]

        # Save the DataFrame as a CSV file
        df_selected.to_csv(save_path, index=False)

        flash('CSV saved successfully!', 'success')
    except Exception as e:
        flash(f'Error saving CSV: {e}', 'danger')

    return redirect(url_for('data_management.data_management'))


@file_handling_bp.route('/delete-file/<filename>', methods=['POST', 'GET'])
def delete_file(filename):
    """
    Deletes a file with the given filename.

    :param filename: The name of the file to delete.
    :return: None.
    """
    # Determine if the file is in DATA_RAW or DATA_SAVED
    file_path_raw = os.path.join('app', current_app.config['DATA_RAW'], filename)
    file_path_saved = os.path.join('app', current_app.config['DATA_SAVED'], filename)
    file_path = file_path_raw if os.path.exists(file_path_raw) else file_path_saved

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'File {filename} successfully deleted.', 'info')
        else:
            flash(f'File {filename} not found.', 'warning')
    except Exception as e:
        flash(f'Error deleting file: {e}', 'danger')

    return redirect(url_for('data_management.data_management'))
