import os

import spacy
from flask import Blueprint, session, redirect, url_for, current_app
from flask import flash, render_template

from .forms import ModelSelectionForm, ModelSaveForm
from ...modules import model_management

# Define the blueprint
model_manager_bp = Blueprint('model_manager', __name__, template_folder='templates')


@model_manager_bp.route('/model-manager', methods=['GET', 'POST'])
def model_manager():
    selection_form = ModelSelectionForm()
    save_form = ModelSaveForm()

    if selection_form.validate_on_submit():
        model_type = selection_form.model_type.data

        if model_type == 'spacy_core':
            chosen_model = selection_form.spacy_model.data
            try:
                nlp = spacy.load(chosen_model)
                session['spacy_model_name'] = chosen_model
                flash(f'spaCy model {chosen_model} loaded successfully', 'success')
            except Exception as e:
                flash(f'Error loading spaCy model: {str(e)}', 'error')

        elif model_type == 'custom':
            custom_model_name = selection_form.custom_model.data
            try:
                custom_model_path = os.path.join(current_app.config['MODEL_DIR'], custom_model_name)
                nlp = spacy.load(custom_model_path)
                session['custom_model_name'] = custom_model_name
                flash(f'Custom model {custom_model_name} loaded successfully', 'success')
            except Exception as e:
                flash(f'Error loading custom model: {str(e)}', 'error')

    if save_form.validate_on_submit() and 'spacy_model_name' in session:
        custom_name = save_form.custom_model_name.data
        try:
            model_name = session['spacy_model_name']
            nlp = spacy.load(model_name)
            models_dir = current_app.config['MODEL_DIR']
            model_path = os.path.join(models_dir, custom_name)
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)
            nlp.to_disk(model_path)
            flash(f"Model saved successfully as {custom_name}", 'success')
        except Exception as e:
            flash(f'Error saving model: {str(e)}', 'error')

    return render_template('model_management.html', selection_form=selection_form, save_form=save_form)


@model_manager_bp.route('/save-model', methods=['POST'])
def save_model():
    form = ModelSaveForm()
    if form.validate_on_submit():
        custom_name = form.custom_model_name.data
        chosen_model = session.get('spacy_model_name')

        if not chosen_model:
            flash('No model selected to save.', 'error')
            return redirect(url_for('model_manager.model_manager'))

        try:
            save_message = model_management.save_model_with_custom_name(chosen_model, custom_name)
            flash(save_message, 'success')
        except Exception as e:
            flash(f'Error saving model: {str(e)}', 'error')

    return redirect(url_for('model_manager.model_manager'))
