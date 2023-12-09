import os

import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from flask import Blueprint, render_template, jsonify, current_app, flash, redirect, url_for, request, session, \
    send_from_directory
from wtforms.fields.simple import StringField

from app.blueprints.model_builder.forms import ModelSelectionForm, ModelDataSelectionForm, TopicModellingForm, \
    TopicLabelForm
from app.modules.file_management import FileManagement
from app.modules.model_building import TopicModelling

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


def reformat_data(row):
    # Assuming each token is separated by a space in the string
    # This is a simple case, it might be more complex depending on how data is stored
    return row.split()


def get_top_words_per_topic(lda_model, num_words=10):
    top_words_per_topic = []
    for i in range(lda_model.num_topics):
        words = lda_model.show_topic(i, num_words)
        top_words = ", ".join([word for word, prob in words])
        top_words_per_topic.append((i, top_words))
    return top_words_per_topic


@model_builder_bp.route('/model-builder', methods=['GET', 'POST'])
def model_builder():
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
        selected_label = next((label for value, label in model_form.model_type.choices if value == selected_model),
                              "Unknown")
        flash(f'Modelling approach selected: {selected_label}', 'info')

        if selected_model == 'topic_modelling':
            # Redirect to topic modeller route
            return redirect(url_for('model_builder.topic_modeller'))

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


@model_builder_bp.route('/topic-modeller', methods=['GET', 'POST'])
def topic_modeller():
    form = TopicModellingForm()
    file_manager = FileManagement()
    topic_label_form = TopicLabelForm()  # Initialize variable here
    lda_model = None

    if 'dataframe_file_path' in session:
        file_path = session['dataframe_file_path']
        try:
            df = pd.read_csv(file_path)
            docs = df['processed_data'].apply(reformat_data).tolist()
        except Exception as e:
            flash(f'Error loading data: {e}', 'error')
            return redirect(url_for('model_builder.model_builder'))

        if form.validate_on_submit():
            topic_modeler = TopicModelling(docs,
                                           form.num_topics.data,
                                           form.random_state.data,
                                           form.chunksize.data,
                                           form.passes.data,
                                           form.tfidf_transform.data,
                                           form.per_word_topics.data,
                                           no_below=form.no_below.data,
                                           no_above=form.no_above.data,
                                           keep_n=form.keep_n.data)

            topic_modeler.create_dictionary_corpus()
            lda_model = topic_modeler.build_model()

            # After building the model, extract top words for each topic
            topics = lda_model.show_topics(num_topics=form.num_topics.data, num_words=10, formatted=False)
            # TODO: Remove this?
            # topics_data = []

            topics = lda_model.show_topics(num_topics=form.num_topics.data, num_words=10, formatted=False)
            for topic_num, topic_words in topics:
                label_field_name = f'topic_{topic_num}_label'
                setattr(topic_label_form, label_field_name, StringField(f'Topic {topic_num + 1}'))
                topic_label_form[label_field_name].label = topic_words

            # TODO: This is all lda_topics_html related. Remove completely if form works.
            # Convert topics data to a DataFrame and then to HTML for display
            # topics_df = pd.DataFrame(topics_data)

            # lda_topics_html = topics_df.to_html(classes=['table', 'table-roboto'], justify='left',
            #                                     index=False)

            if 'topic_label_form' in session and session['topic_label_form'].validate_on_submit():
                topic_label_form = session['topic_label_form']

                # Apply labels to DataFrame
                for topic_num in range(1, form.num_topics.data + 1):
                    label = getattr(topic_label_form, f'topic_{topic_num}_label').data
                    # Assume df has a 'topic' column with topic numbers
                    df.loc[df['topic'] == topic_num, 'topic_label'] = label

                    # Save DataFrame
                    save_name = topic_label_form.save_name.data
                    file_manager.save_as_csv(df, f'{save_name}.csv', 'LABELLED_DATA_DIR')

                    # Clear the form from the session
                    del session['topic_label_form']
                    flash('Data saved with topic labels.', 'success')

                    # Clear the form from the session
                    del session['topic_label_form']
                    flash('Data saved with topic labels.', 'success')

            # Visualization and saving visualization logic goes here
            # pyLDAvis.enable_notebook()
            vis = gensimvis.prepare(lda_model, topic_modeler.corpus, topic_modeler.dictionary)

            # Save visualization
            visualization_name = form.visualization_name.data
            output_path = os.path.join(current_app.config['MODELS_DIR'], f"{visualization_name}.html")
            pyLDAvis.save_html(vis, output_path)
            session['last_visualization_name'] = visualization_name

            flash("Topic model built successfully.", "success")

    else:
        flash("No data file selected for topic modeling.", "warning")
        return redirect(url_for('model_builder.model_builder'))
    # Render the template with the form and optional table
    return render_template('topic_modeller.html', form=form, topic_label_form=topic_label_form, lda_model=lda_model)


@model_builder_bp.route('/model-view/<visualization_name>')
def model_view(visualization_name):
    visualization_file = f"{visualization_name}.html"
    return render_template('model_view.html', visualization_file=visualization_file)


@model_builder_bp.route('/model-output/<filename>')
def model_output(filename):
    return send_from_directory(current_app.config['MODELS_DIR'], filename)
