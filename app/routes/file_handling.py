import os

import pandas as pd
from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash

from app.utils import prepare_file_management_forms

file_handling_bp = Blueprint('file_handling', __name__)


@file_handling_bp.route('/select-file', methods=['GET', 'POST'])
def select_file():
    form, raw_file_form, saved_file_form, raw_files, saved_files = prepare_file_management_forms()

    if raw_file_form.validate_on_submit():
        selected_file = raw_file_form.selected_file.data
        file_path = os.path.join('app', current_app.config['DATA_RAW'], selected_file)

        xls = pd.ExcelFile(file_path)
        sheets = xls.sheet_names

        return render_template('data_management.html', form=form, raw_file_form=raw_file_form,
                               saved_file_form=saved_file_form, worksheets=sheets, selected_file=selected_file)

    return redirect(url_for('data_management.data_management'))


@file_handling_bp.route('/save-csv', methods=['POST'])
def save_csv():
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
