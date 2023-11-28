import os

import pandas as pd
from flask import current_app
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from app.forms import FileUploadForm, SpacyModelForm, RawFileSelectionForm, SavedFileSelectionForm, WorksheetSelectionForm


def get_saved_files():
    data_saved_path = os.path.join(current_app.root_path, current_app.config['DATA_SAVED'])
    return os.listdir(data_saved_path)


def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/data-management', methods=['GET', 'POST'])
    def data_management():
        form = FileUploadForm()
        raw_file_form = RawFileSelectionForm()
        saved_file_form = SavedFileSelectionForm()

        raw_files = os.listdir(os.path.join('app', app.config['DATA_RAW']))
        saved_files = os.listdir(os.path.join('app', app.config['DATA_SAVED']))

        raw_file_form.selected_file.choices = [(file, file) for file in raw_files]
        saved_file_form.selected_saved_file.choices = [(file, file) for file in saved_files]

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

        return render_template('data_management.html', form=form, raw_file_form=raw_file_form,
                               saved_file_form=saved_file_form, raw_files=raw_files, saved_files=saved_files)

    @app.route('/select-file', methods=['POST'])
    def select_file():
        form = FileUploadForm()
        raw_file_form = RawFileSelectionForm()
        saved_file_form = SavedFileSelectionForm()

        raw_files = os.listdir(os.path.join('app', app.config['DATA_RAW']))
        saved_files = os.listdir(os.path.join('app', app.config['DATA_SAVED']))

        raw_file_form.selected_file.choices = [(file, file) for file in raw_files]
        saved_file_form.selected_saved_file.choices = [(file, file) for file in saved_files]

        if raw_file_form.validate_on_submit():
            selected_file = raw_file_form.selected_file.data
            file_path = os.path.join('app', app.config['DATA_RAW'], selected_file)

            xls = pd.ExcelFile(file_path)
            sheets = xls.sheet_names

            return render_template('data_management.html', form=form, raw_file_form=raw_file_form,
                                   saved_file_form=saved_file_form, worksheets=sheets, selected_file=selected_file)

        return redirect(url_for('data_management'))

    @app.route('/select-worksheet', methods=['POST'])
    def select_worksheet():
        form = FileUploadForm()  # Create an instance of your form class
        selected_file = request.form['selected_file']
        selected_sheet = request.form['selected_sheet']
        file_path = os.path.join('app', app.config['DATA_RAW'], selected_file)

        # Read the worksheet
        df = pd.read_excel(file_path, sheet_name=selected_sheet)
        columns = df.columns.tolist()
        saved_files = get_saved_files()
        column_info = [(col, df[col].iloc[0] if not df[col].empty else None, df[col].isna().sum()) for col in columns]

        # Pass the form object along with other data to the template
        return render_template('worksheet_display.html', column_info=column_info, saved_files=saved_files,
                               selected_file=selected_file, selected_sheet=selected_sheet, total_rows=len(df))

    @app.route('/save-csv', methods=['POST'])
    def save_csv():
        selected_file = request.form['selected_file']
        selected_sheet = request.form['selected_sheet']
        selected_columns = request.form.getlist('selected_columns')
        csv_name = request.form['csv_name'] + '.csv'
        file_path = os.path.join('app', app.config['DATA_RAW'], selected_file)
        save_path = os.path.join('app', app.config['DATA_SAVED'], csv_name)

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

        return redirect(url_for('data_management'))

    @app.route('/view-saved-file', methods=['GET', 'POST'])
    def view_saved_file():
        saved_file_form = SavedFileSelectionForm()
        saved_files = os.listdir(os.path.join('app', app.config['DATA_SAVED']))
        saved_file_form.selected_saved_file.choices = [(file, file) for file in saved_files]

        # Check if there are saved files
        if not saved_files:
            flash('No saved files available', 'warning')
            return render_template('view_saved_file.html', saved_file_form=saved_file_form)

        if saved_file_form.validate_on_submit():
            selected_file = saved_file_form.selected_saved_file.data
            file_path = os.path.join('app', app.config['DATA_SAVED'], selected_file)
            # Check if a file is actually selected
            if not selected_file:
                flash('No file selected', 'warning')
                return redirect(url_for('data_management'))
            try:
                df = pd.read_csv(file_path, nrows=5)

                # Convert the DataFrame to HTML with Bootstrap classes
                table_html = df.to_html(classes='table table-hover table-sm left-justified-headers',
                                        index=False, header=True)
                # Render a template with the DataFrame
                return render_template('view_saved_file.html', saved_file_form=view_saved_file, table_html=table_html,
                                       file_name=selected_file)
            except Exception as e:
                flash(f'Error reading file: {e}', 'danger')

        return render_template('view_saved_file.html', saved_file_form=saved_file_form)

    @app.route('/data-modeling', methods=['GET', 'POST'])
    def data_modeling():
        spacy_model_form = SpacyModelForm()

        if spacy_model_form.validate_on_submit():
            selected_model = spacy_model_form.model.data
            flash(f'Model selected: {selected_model}', 'info')
            # Additional logic to load the selected spaCy model can be added here
            # ...

        return render_template('data_modeling.html', spacy_model_form=spacy_model_form)

    @app.route('/reporting')
    def reporting():
        return render_template('reporting.html')
