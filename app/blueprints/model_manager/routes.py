from flask import Blueprint, session, redirect, url_for
from flask import flash, render_template

from app.modules.model_management import load_spacy_model
from .forms import ModelSelectionForm
from ...modules import model_management

# Define the blueprint
model_manager_bp = Blueprint('model_manager', __name__, template_folder='templates')


@model_manager_bp.route('/model-manager', methods=['GET', 'POST'])
def model_manager():
    form = ModelSelectionForm()
    if form.validate_on_submit():
        model_type = form.model_type.data

        if model_type == 'spacy_core':
            chosen_model = form.spacy_model.data
            session['spacy_model_name'] = chosen_model  # Store the chosen model in session
            try:
                nlp = load_spacy_model()
                if nlp:
                    flash(f'spaCy model {chosen_model} loaded successfully', 'success')
                    print(nlp.pipe_names)
                else:
                    flash(f'Failed to load spaCy model {chosen_model}', 'error')
            except Exception as e:
                flash(f'Error loading spaCy model: {str(e)}', 'error')

    else:
        print("Form Validation Errors:", form.errors)  # Logic to load the model based on type and name
        # ...

        # return redirect(url_for('model_manager.model_manager'))
    return render_template('model_management.html', form=form)


@model_manager_bp.route('/save-model', methods=['POST'])
def save_model():
    # Assumes the chosen model name is stored in the session
    chosen_model = session.get('spacy_model_name')
    if not chosen_model:
        flash('No model selected to save.', 'error')
        return redirect(url_for('model_manager.model_manager'))

    try:
        save_message = model_management.save_model(chosen_model)
        flash(save_message, 'success')
    except Exception as e:
        flash(f'Error saving model: {str(e)}', 'error')

    return redirect(url_for('model_manager.model_manager'))
