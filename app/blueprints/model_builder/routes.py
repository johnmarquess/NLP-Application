import os

from flask import Blueprint, render_template, jsonify, current_app, flash, redirect, url_for, request, session

from app.blueprints.model_builder.forms import ModelSelectionForm, ModelDataSelectionForm
from app.modules.file_management import FileManagement

# Define the blueprint
model_builder_bp = Blueprint('model_builder', __name__, template_folder='templates')


# Forms and routes will be defined here
def set_file_and_column_choices(data_form, file_manager, processed_data_dir):
    """
    Sets the choices for the file field in the data form based on the available processed files in the specified directory.
    Also selects the first file in the list, if available, and sets the choices for the column field in the data form based on the columns in the selected file.

    Args:
        data_form (Form): The data form object.
        file_manager (FileManager): The file manager object.
        processed_data_dir (str): The path to the processed data directory.

    Returns:
        None
    """
    processed_files = file_manager.list_files(processed_data_dir)
    data_form.file.choices = [(f, f) for f in processed_files if f.endswith('.csv')]
    selected_file = data_form.file.data or (processed_files[0] if processed_files else None)
    if selected_file:
        file_path = os.path.join(processed_data_dir, selected_file)
        columns = file_manager.get_csv_columns(file_path)
        set_column_choices(data_form, columns)


def set_column_choices(data_form, columns):
    """
    Set the choices for the column field in the given data form using the provided columns.

    Parameters:
    data_form (Form): The data form object.
    columns (list): The list of columns to set as choices.

    Returns:
    None: This method does not return anything.

    Example:
    data_form = DataForm()
    columns = ['column1', 'column2', 'column3']
    set_column_choices(data_form, columns)
    """
    data_form.column.choices = [(col, col) for col in columns]
    if 'processed_data' in columns:
        data_form.column.default = 'processed_data'


@model_builder_bp.route('/model-builder', methods=['GET', 'POST'])
def model_builder():
    """
    Endpoint for the model builder page.

    Route: '/model-builder'
    Methods: ['GET', 'POST']

    Parameters:
        None

    Returns:
        template: 'model_builder.html'
        arguments: model_form, data_form, table_html

    """
    model_form = ModelSelectionForm()
    data_form = ModelDataSelectionForm()
    file_manager = FileManagement()
    table_html = ""
    processed_data_dir = current_app.config['PROCESSED_DATA_DIR']
    set_file_and_column_choices(data_form, file_manager, processed_data_dir)
    if 'data_submit' in request.form and data_form.validate_on_submit():
        selected_file = data_form.file.data
        file_path = os.path.join(processed_data_dir, selected_file)
        session['dataframe_file_path'] = file_path  # Save the file path in the session
        selected_columns = None if data_form.all_columns.data else [data_form.column.data]
        columns = file_manager.get_csv_columns(file_path)
        set_column_choices(data_form, columns)
        try:
            table_html = file_manager.view_csv_contents(file_path, selected_columns)
            if 'An error occurred' in table_html:
                flash(table_html, 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
            return redirect(url_for('model_builder.model_builder'))
    if model_form.validate_on_submit():
        selected_model = model_form.model_type.data
        # Find the label for the selected model
        selected_label = next((label for value, label in model_form.model_type.choices if value == selected_model),
                              "Unknown")
        flash(f'Modeling approach selected: {selected_label}', 'info')
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
