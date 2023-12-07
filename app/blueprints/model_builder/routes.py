import os

from flask import Blueprint, render_template, jsonify, current_app, flash, redirect, url_for, request

from app.blueprints.model_builder.forms import ModelSelectionForm, ModelDataSelectionForm
from app.modules.file_management import FileManagement

# Define the blueprint
model_builder_bp = Blueprint('model_builder', __name__, template_folder='templates')


# Forms and routes will be defined here
@model_builder_bp.route('/model-builder', methods=['GET', 'POST'])
def model_builder():
    model_form = ModelSelectionForm()
    data_form = ModelDataSelectionForm()
    file_manager = FileManagement()
    table_html = ""

    processed_data_dir = current_app.config['PROCESSED_DATA_DIR']
    processed_files = file_manager.list_files(processed_data_dir)
    data_form.file.choices = [(f, f) for f in processed_files if f.endswith('.csv')]

    selected_file = data_form.file.data or (processed_files[0] if processed_files else None)
    if selected_file:
        file_path = os.path.join(processed_data_dir, selected_file)
        columns = file_manager.get_csv_columns(file_path)
        data_form.column.choices = [(col, col) for col in columns]
        if 'processed_data' in columns:
            data_form.column.default = 'processed_data'

    if model_form.validate_on_submit():
        selected_model = model_form.model_type.data
        selected_label = next((label for value, label in model_form.model_type.choices if value == selected_model),
                              "Unknown")
        flash(f'Modeling approach selected: {selected_label}', 'info')

    if 'data_submit' in request.form and data_form.validate_on_submit():
        selected_file = data_form.file.data
        all_columns_selected = data_form.all_columns.data
        selected_columns = None if all_columns_selected else [data_form.column.data]

        # Load the data and generate the table HTML
        try:
            file_path = os.path.join(current_app.config['PROCESSED_DATA_DIR'], selected_file)
            table_html = file_manager.view_csv_contents(file_path, selected_columns)

            if 'An error occurred' in table_html:
                flash(table_html, 'error')
                # return redirect(url_for('model_builder.model_builder'))

        except Exception as e:
            flash(f'Error: {e}', 'error')
            return redirect(url_for('model_builder.model_builder'))

    # Render the template with the table HTML
    return render_template('model_builder.html', model_form=model_form, data_form=data_form, table_html=table_html)


@model_builder_bp.route('/get-columns-model/<filename>')
def get_columns(filename):
    file_manager = FileManagement()
    file_path = os.path.join(current_app.config['PROCESSED_DATA_DIR'], filename)
    try:
        columns = file_manager.get_csv_columns(file_path)
        return jsonify(columns)
    except Exception as e:
        return jsonify({'error': str(e)})
