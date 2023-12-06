import os

from flask import Blueprint, render_template, flash, jsonify, request, current_app

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

    # Use the configuration to get the processed files directory
    processed_data_dir = current_app.config['PROCESSED_DATA_DIR']
    processed_files = file_manager.list_files(processed_data_dir)
    data_form.file.choices = [(f, f) for f in processed_files if f.endswith('.csv')]

    # Handle model form submission
    if 'model_submit' in request.form and model_form.validate_on_submit():
        selected_model = model_form.model_type.data
        selected_label = next((label for value, label in model_form.model_type.choices if value == selected_model),
                              "Unknown")
        flash(f'Modeling approach selected: {selected_label}', 'info')

    # Handle data form submission
    if 'data_submit' in request.form and data_form.validate_on_submit():
        # Add logic to handle selected file and column
        pass

    return render_template('model_builder.html', model_form=model_form, data_form=data_form)


@model_builder_bp.route('/get-columns/<filename>')
def get_columns(filename):
    file_manager = FileManagement()
    file_path = os.path.join('data/processed', filename)
    try:
        columns = file_manager.get_csv_columns(file_path)
        return jsonify(columns)
    except Exception as e:
        return jsonify({'error': str(e)})
