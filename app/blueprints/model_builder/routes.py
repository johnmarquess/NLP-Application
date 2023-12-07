import os

from flask import Blueprint, render_template, jsonify, request, current_app, flash

from app.blueprints.model_builder.forms import ModelSelectionForm, ModelDataSelectionForm
from app.modules.file_management import FileManagement

# Define the blueprint
model_builder_bp = Blueprint('model_builder', __name__, template_folder='templates')


# Forms and routes will be defined here
@model_builder_bp.route('/model-builder', methods=['GET', 'POST'])
def model_builder():
    form = ModelSelectionForm()
    data_form = ModelDataSelectionForm()
    file_manager = FileManagement()

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

    if form.validate_on_submit():
        selected_model = form.model_type.data
        selected_label = next((label for value, label in form.model_type.choices if value == selected_model), "Unknown")
        flash(f'Modeling approach selected: {selected_label}', 'info')

    if 'data_submit' in request.form and data_form.validate_on_submit():
        # Handle data form submission
        pass

    return render_template('model_builder.html', form=form, data_form=data_form)


@model_builder_bp.route('/get-columns-model/<filename>')
def get_columns(filename):
    file_manager = FileManagement()
    file_path = os.path.join(current_app.config['PROCESSED_DATA_DIR'], filename)
    try:
        columns = file_manager.get_csv_columns(file_path)
        return jsonify(columns)
    except Exception as e:
        return jsonify({'error': str(e)})
