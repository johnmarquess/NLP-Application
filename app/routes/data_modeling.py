import spacy
from flask import Blueprint, render_template, flash, redirect, url_for

from app.forms import SpacyModelForm

data_modeling_bp = Blueprint('data_modeling', __name__)


@data_modeling_bp.route('/data-modeling', methods=['GET', 'POST'])
def data_modeling():
    spacy_model_form = SpacyModelForm()

    if spacy_model_form.validate_on_submit():
        model_choice = spacy_model_form.model.data

        try:
            if model_choice == 'en_core_web_sm':
                nlp = spacy.load("en_core_web_sm")
            elif model_choice == 'en_core_web_md':
                nlp = spacy.load("en_core_web_md")
            elif model_choice == 'en_core_web_lg':
                nlp = spacy.load("en_core_web_lg")
            elif model_choice == 'en':
                nlp = spacy.blank('en')
            else:
                flash("Invalid model selection", 'error')
                return redirect(url_for('data_modeling.data_modeling'))

            # Here, you can do additional processing with the nlp object
            # ...

            flash(f"Model {model_choice} loaded successfully!", 'success')
            return redirect(url_for('data_modeling.data_modeling'))

        except Exception as e:
            flash(f"Failed to load model {model_choice}: {str(e)}. Make sure you have downloaded the model!", 'danger')
            return redirect(url_for('data_modeling.data_modeling'))

    return render_template('data_modeling.html', spacy_model_form=spacy_model_form)
