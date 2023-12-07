import os

from flask import Blueprint, render_template, jsonify, current_app, flash, redirect, url_for, session

from app.blueprints.model_builder.forms import ModelSelectionForm, ModelDataSelectionForm, TopicModelingForm
from app.modules.file_management import FileManagement

import pandas as pd
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

    if data_form.validate_on_submit():
        selected_file = data_form.file.data
        session['selected_file'] = selected_file

        if data_form.all_columns.data:
            # If 'Select All Columns' is checked
            session['selected_columns'] = None  # Indicates all columns are selected
        else:
            # Specific column is selected
            selected_column = data_form.column.data
            session['selected_columns'] = [selected_column]  # Store as a list for consistency

        # Redirect to display data or another appropriate route
        return redirect(url_for('model_builder.display_data'))

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


@model_builder_bp.route('/display-data')
def display_data():
    if 'selected_file' not in session:
        flash('No file selected', 'warning')
        return redirect(url_for('model_builder.model_builder'))

    file_manager = FileManagement()
    file_path = os.path.join(current_app.config['PROCESSED_DATA_DIR'], session['selected_file'])

    try:
        selected_columns = session.get('selected_columns', None)
        table_html = file_manager.view_csv_contents(file_path, selected_columns)

        if 'An error occurred' in table_html:
            flash(table_html, 'error')
            return redirect(url_for('model_builder.model_builder'))

    except Exception as e:
        flash(f'Error: {e}', 'error')
        return redirect(url_for('model_builder.model_builder'))

    return render_template('display_data.html', table_html=table_html)


# @model_builder_bp.route('/topic-modeling', methods=['GET', 'POST'])
# def topic_modeling():
#     form = TopicModelingForm()
#     if form.validate_on_submit():
#         # Load processed data
#         file_path =  # path to the processed data file
#         df = pd.read_csv(file_path)
#         docs = df['processed_data'].apply(lambda x: x.split())
#
#         # Create TopicModeling object
#         topic_model = TopicModeling(docs,
#                                     form.num_topics.data,
#                                     form.random_state.data,
#                                     form.chunksize.data,
#                                     form.passes.data,
#                                     tfidf_transform=form.tfidf_transform.data,
#                                     per_word_topics=form.per_word_topics.data)
#         topic_model.create_dictionary_corpus()
#         lda_model = topic_model.build_model()
#
#         # Visualization and exporting (next steps)
#
#         return render_template('topic_modeller.html', form=form)
