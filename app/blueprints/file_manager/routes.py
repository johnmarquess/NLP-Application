import os

import pandas as pd
from flask import Blueprint, render_template, flash, current_app, request, jsonify, redirect, url_for

from app.modules.file_management import FileManagement
from .forms import FileUploadForm, LoadSpreadsheetForm

file_manager_bp = Blueprint('file_manager', __name__)


def handle_file_upload(form, file_manager):
    if form.validate_on_submit():
        file = form.file.data
        message = file_manager.upload_file(file, 'raw')
        flash(message, 'success')
        return True  # Indicate that the upload was successful
    return False  # Indicate no upload or failure


@file_manager_bp.route('/get-files', methods=['GET'])
def get_files():
    file_manager = FileManagement()
    raw_files = file_manager.list_files('raw')
    return jsonify(raw_files)


@file_manager_bp.route('/file-manager', methods=['GET', 'POST'])
def file_manager():
    upload_form = FileUploadForm()
    spreadsheet_form = LoadSpreadsheetForm()
    file_manager_instance = FileManagement()

    # Define raw_files here to ensure it's available throughout the function
    raw_files = file_manager_instance.list_files('raw')
    spreadsheet_files = [f for f in raw_files if f.endswith(('.xls', '.xlsx'))]
    spreadsheet_form.file_choice.choices = [(f, f) for f in spreadsheet_files]

    # Handle file upload
    if 'upload' in request.form:
        handle_file_upload(upload_form, file_manager_instance)

    if 'select_spreadsheet' in request.form:
        selected_file = spreadsheet_form.file_choice.data
        if selected_file:
            spreadsheet_form.selected_file.data = selected_file
            worksheets = file_manager_instance.list_worksheets(
                os.path.join(current_app.config['RAW_DATA_DIR'], selected_file))
            spreadsheet_form.worksheet_choice.choices = [(ws, ws) for ws in worksheets]
        else:
            flash("No file selected.", "warning")

    if 'view_worksheet' in request.form and spreadsheet_form.worksheet_choice.data:
        selected_file = spreadsheet_form.selected_file.data  # Retrieve the hidden field value
        selected_worksheet = spreadsheet_form.worksheet_choice.data
        if selected_file:
            return redirect(
                url_for('file_manager.view_worksheet', file_path=selected_file, sheet_name=selected_worksheet))
        else:
            flash('No spreadsheet selected', 'danger')

    clean_files = file_manager_instance.list_files('clean')
    table_html = None
    if request.method == 'POST':
        selected_file_clean = request.form.get('file_choice')
        if selected_file_clean:
            file_path = os.path.join(current_app.config['CLEAN_DATA_DIR'], selected_file_clean)
            table_html = file_manager_instance.view_csv_contents(file_path)

    return render_template('file_manager.html',
                           upload_form=upload_form, raw_files=raw_files, clean_files=clean_files,
                           table_html=table_html, spreadsheet_form=spreadsheet_form)


@file_manager_bp.route('/view-worksheet', methods=['GET'])
def view_worksheet():
    file_path = request.args.get('file_path')
    sheet_name = request.args.get('sheet_name')
    # file_name = request.args.get('file_name')

    # Ensure both file_path and sheet_name are provided
    if not file_path or not sheet_name:
        flash('Spreadsheet or worksheet not specified', 'danger')
        return redirect(url_for('file_manager.file_manager'))

    try:
        # Construct the full path to the file
        full_file_path = os.path.join(current_app.config['RAW_DATA_DIR'], file_path)

        # Read the specified worksheet from the spreadsheet
        df = pd.read_excel(full_file_path, sheet_name=sheet_name)

        # Prepare the data for display
        summary = {col: {'column_name': col, 'first_item': df[col].iloc[0], 'missing_count': df[col].isna().sum()} for
                   col in df.columns}
        metadata = {'worksheet_name': sheet_name, 'total_rows': len(df), 'file_name': file_path}

        summary = pd.DataFrame(summary)
    except Exception as e:
        flash(f'Error reading spreadsheet: {e}', 'danger')
        return redirect(url_for('file_manager.file_manager'))

    return render_template('view_spreadsheet.html', summary=summary, metadata=metadata, file_path=file_path,
                           sheet_name=sheet_name)


@file_manager_bp.route('/export-selected-columns', methods=['POST'])
def export_selected_columns():
    file_manager_instance = FileManagement()
    selected_columns = request.form.getlist('selected_columns')
    drop_empty = 'drop_empty' in request.form
    custom_file_name = request.form.get('custom_file_name', 'exported_data') + '.csv'  # Default name if not provided
    file_path = request.form.get('file_path')
    sheet_name = request.form.get('sheet_name')

    # Validate file_path and sheet_name
    if not file_path or not sheet_name:
        flash('File path or sheet name missing', 'danger')
        return redirect(url_for('file_manager.file_manager'))

    # Load the original DataFrame
    df = pd.read_excel(os.path.join(current_app.config['RAW_DATA_DIR'], file_path), sheet_name=sheet_name)

    # Prepare a dictionary for new column names and update selected columns
    new_names = {}
    updated_selected_columns = []
    for col in selected_columns:
        new_name = request.form.get(f'new_name_{col}', col)  # Default to original name if new name not provided
        new_names[col] = new_name
        updated_selected_columns.append(new_name)  # Use new name for updated list

    # Rename columns
    df.rename(columns=new_names, inplace=True)

    # Filter the DataFrame to include only the updated selected columns
    df = df[updated_selected_columns]

    # Drop empty rows if option is selected
    if drop_empty:
        df.dropna(subset=updated_selected_columns, how='all', inplace=True)

    save_message = file_manager_instance.save_as_csv(df, custom_file_name, 'CLEAN_DATA_DIR')
    flash(save_message, 'success')
    return redirect(url_for('file_manager.file_manager'))


@file_manager_bp.route('/delete-file/<file_type>', methods=['POST'])
def delete_file(file_type):
    file_manager_instance = FileManagement()

    # Retrieve the file name based on the file type
    if file_type == 'raw':
        file_name = request.form.get('file_choice')  # assuming this is the name for raw file selection
    elif file_type == 'clean':
        file_name = request.form.get('file_choice')  # same name used in clean files form
    else:
        flash('Invalid file type', 'danger')
        return redirect(url_for('file_manager.file_manager'))

    if not file_name:
        flash('No file selected', 'danger')
        return redirect(url_for('file_manager.file_manager'))

    directory = current_app.config['RAW_DATA_DIR'] if file_type == 'raw' else current_app.config['CLEAN_DATA_DIR']
    file_path = os.path.join(directory, file_name)
    deletion_status = file_manager_instance.delete_file(file_path)

    if deletion_status:
        flash(f'File {file_name} deleted successfully.', 'success')
    else:
        flash(f'Failed to delete {file_name}.', 'danger')
    return redirect(url_for('file_manager.file_manager'))
