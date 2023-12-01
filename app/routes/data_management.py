import os

import pandas as pd
from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from werkzeug.utils import secure_filename

from app.forms import SavedFileSelectionForm
from app.utils import get_saved_files, prepare_file_management_forms

data_management_bp = Blueprint('data_management', __name__)


@data_management_bp.route('/data-management', methods=['GET', 'POST'])
def data_management():
    form, raw_file_form, saved_file_form, raw_files, saved_files = prepare_file_management_forms()

    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)

        # Prepend 'app/' to the DATA_RAW path
        save_path = os.path.join('app', current_app.config['DATA_RAW'])

        try:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            f.save(os.path.join(save_path, filename))
            flash(f'File {filename} has been saved successfully!', 'success')
        except Exception as e:
            flash(f'Error saving file: {e}', 'warning')

        return redirect(url_for('data_management.data_management'))

    return render_template('data_management.html', form=form, raw_file_form=raw_file_form,
                           saved_file_form=saved_file_form, raw_files=raw_files, saved_files=saved_files)


@data_management_bp.route('/select-worksheet', methods=['POST'])
def select_worksheet():
    selected_file = request.form['selected_file']
    selected_sheet = request.form['selected_sheet']
    file_path = os.path.join('app', current_app.config['DATA_RAW'], selected_file)

    # Read the worksheet
    df = pd.read_excel(file_path, sheet_name=selected_sheet)
    columns = df.columns.tolist()
    saved_files = get_saved_files()
    column_info = [(col, df[col].iloc[0] if not df[col].empty else None, df[col].isna().sum()) for col in columns]

    # Pass the form object along with other data to the template
    return render_template('worksheet_display.html', column_info=column_info, saved_files=saved_files,
                           selected_file=selected_file, selected_sheet=selected_sheet, total_rows=len(df))


@data_management_bp.route('/view-saved-file', methods=['POST'])
def view_saved_file():
    saved_file_form = SavedFileSelectionForm()
    saved_files = os.listdir(os.path.join('app', current_app.config['DATA_SAVED']))
    saved_file_form.selected_saved_file.choices = [(file, file) for file in saved_files]

    # Check if there are saved files
    if not saved_files:
        flash('No saved files available', 'warning')
        return render_template('view_saved_file.html', saved_file_form=saved_file_form)

    if saved_file_form.validate_on_submit():
        selected_file = saved_file_form.selected_saved_file.data
        file_path = os.path.join('app', current_app.config['DATA_SAVED'], selected_file)
        # Check if a file is actually selected
        if not selected_file:
            flash('No file selected', 'warning')
            return redirect(url_for('data_management.data_management'))
        try:
            df = pd.read_csv(file_path, nrows=10)

            # Convert the DataFrame to HTML with Bootstrap classes
            table_html = df.to_html(classes='table table-hover table-sm left-justified-headers',
                                    index=False, header=True)
            # Render a template with the DataFrame
            return render_template('view_saved_file.html', saved_file_form=view_saved_file, table_html=table_html,
                                   file_name=selected_file)
        except Exception as e:
            flash(f'Error reading file: {e}', 'danger')

    return render_template('view_saved_file.html', saved_file_form=saved_file_form)
