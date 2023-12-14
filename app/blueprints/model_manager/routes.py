import os

from flask import Blueprint, session, redirect, url_for, current_app
from flask import flash, render_template

from app.modules.file_management import FileManagement
from app.modules.model_management import ModelManager
from .forms import ModelSelectionForm, ModelSaveForm, ReferenceFileForm

# Define the blueprint
model_manager_bp = Blueprint('model_manager', __name__, template_folder='templates')


@model_manager_bp.route('/model-manager', methods=['GET', 'POST'])
def model_manager():
    selection_form = ModelSelectionForm()
    save_form = ModelSaveForm()
    file_manager_instance = FileManagement()
    reference_form = ReferenceFileForm()
    table_html = None
    update_message = None

    # Populate choices for reference files
    reference_files = file_manager_instance.list_files('reference')
    reference_form.reference_file.choices = [(f, f) for f in reference_files]

    model_loaded = 'spacy_model_name' in session or 'custom_model_name' in session

    if selection_form.validate_on_submit():
        model_type = selection_form.model_type.data
        model_identifier = selection_form.spacy_model.data if model_type == 'spacy_core' else selection_form.custom_model.data

        model_mgr = ModelManager()
        load_message, model = model_mgr.load_model(model_type, model_identifier)
        flash(load_message, 'error' if 'Error loading model' in load_message else 'success')

    # Handling the reference file form submission
    if reference_form.validate_on_submit():
        selected_reference_file = reference_form.reference_file.data
        file_path = os.path.join(current_app.config['REFERENCE_DATA_DIR'], selected_reference_file)

        model_mgr = ModelManager()
        update_message = model_mgr.add_entities_from_csv(file_path)
        flash(update_message)

        # Optionally, display the contents of the file
        table_html = file_manager_instance.view_csv_contents(file_path)

    return render_template('model_management.html',
                           selection_form=selection_form,
                           save_form=save_form,
                           reference_form=reference_form,
                           table_html=table_html,
                           model_loaded=model_loaded,
                           update_message=update_message)


@model_manager_bp.route('/save-model', methods=['POST'])
def save_model():
    form = ModelSaveForm()
    if form.validate_on_submit():
        custom_name = form.custom_model_name.data
        chosen_model = session.get('spacy_model_name')

        if not chosen_model:
            flash('No model selected to save.', 'error')
            return redirect(url_for('model_manager.model_manager'))

        model_mgr = ModelManager()
        save_message = model_mgr.save_model_with_custom_name(chosen_model, custom_name)
        if 'Error saving model' in save_message:
            flash(save_message, 'error')
        else:
            flash(save_message, 'success')

    return redirect(url_for('model_manager.model_manager'))
