from flask import Blueprint, render_template, flash

from app.forms import SpacyModelForm

data_modeling_bp = Blueprint('data_modeling', __name__)


@data_modeling_bp.route('/data-modeling', methods=['GET', 'POST'])
def data_modeling():
    spacy_model_form = SpacyModelForm()

    if spacy_model_form.validate_on_submit():
        selected_model = spacy_model_form.model.data
        flash(f'Model selected: {selected_model}', 'info')
        # Additional logic to load the selected spaCy model can be added here
        # ...

    return render_template('data_modeling.html', spacy_model_form=spacy_model_form)
