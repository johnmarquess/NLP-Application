from flask import Blueprint, render_template, flash, redirect, url_for

from app.blueprints.model_builder.forms import ModelSelectionForm

# Define the blueprint
model_builder_bp = Blueprint('model_builder', __name__, template_folder='templates')


# Forms and routes will be defined here
@model_builder_bp.route('/model-builder', methods=['GET', 'POST'])
def model_builder():
    form = ModelSelectionForm()
    if form.validate_on_submit():
        selected_model = form.model_type.data
        selected_label = next((label for value, label in form.model_type.choices if value == selected_model), "Unknown")
        # Additional logic based on selected model
        flash(f'Modeling approach selected: {selected_label}', 'info')
        return redirect(url_for('model_builder.model_builder'))  # Redirect as needed

    return render_template('model_builder.html', form=form)
