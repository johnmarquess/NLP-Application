import os

import pandas as pd
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from app import app


def allowed_file(filename):
    return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def get_column_info(df):
    column_info = []
    for column in df.columns:
        first_item = df[column].iloc[0] if not df[column].empty else 'N/A'
        missing_values = df[column].isna().sum()
        total_values = len(df[column])
        column_info.append(
            {'name': column, 'first_item': first_item, 'missing_ratio': f"{missing_values}:{total_values}"})
    return column_info


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "datafile" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        file = request.files["datafile"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Change this to save in the DATA_RAW_FOLDER
            file.save(os.path.join(app.config["DATA_RAW_FOLDER"], filename))
            flash(
                f'File uploaded successfully to {app.config["DATA_RAW_FOLDER"]}',
                "success",
            )
            return redirect(
                url_for("data_management")
            )  # Or any other route you'd like to redirect to
    return render_template("upload.html")


@app.route('/select_columns', methods=['GET', 'POST'])
def select_columns():
    selected_file = request.args.get('selected_file') if request.method == 'GET' else request.form.get('selected_file')
    file_path = os.path.join(app.config['DATA_RAW_FOLDER'], selected_file)

    try:
        if selected_file.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif selected_file.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            flash('Unsupported file format', 'error')
            return redirect(url_for('data_management'))

        column_info = get_column_info(df)
        return render_template('view_worksheet.html', column_info=column_info, selected_file=selected_file)

    except Exception as e:
        flash(f'Error reading file: {e}', 'error')
        return redirect(url_for('data_management'))


@app.route("/data_modeling")
def data_modeling():
    return render_template("data_modeling.html")


@app.route('/data_management', methods=['GET', 'POST'])
def data_management():
    if request.method == 'POST':
        selected_file = request.form.get('selected_file')
        if selected_file:
            return redirect(url_for('select_columns', selected_file=selected_file))
        else:
            flash('No file selected', 'error')

    files = os.listdir(app.config['DATA_RAW_FOLDER'])
    return render_template('data_management.html', files=files)


@app.route('/view_file_contents', methods=['POST'])
def view_file_contents():
    selected_columns = request.form.getlist('columns')
    selected_file = request.form.get('selected_file')
    file_path = os.path.join(app.config['DATA_RAW_FOLDER'], selected_file)

    try:
        data = pd.read_csv(file_path, usecols=selected_columns)
        total_rows = len(data)
        data_sample = data.sample(n=5)  # Or any other logic for sampling
    except Exception as e:
        flash(f'Error loading file: {e}', 'error')
        return redirect(url_for('select_columns', selected_file=selected_file))

    return render_template('view_file_contents.html', data=data_sample, file_name=selected_file, total_rows=total_rows)


@app.route('/view_worksheet', methods=['POST'])
def view_worksheet():
    selected_file = request.form.get('selected_file')
    selected_worksheet = request.form.get('selected_worksheet')
    file_path = os.path.join(app.config['DATA_RAW_FOLDER'], selected_file)

    try:
        df = pd.read_excel(file_path, sheet_name=selected_worksheet)
        total_values = len(df)
        column_info = []
        for column in df.columns:
            first_item = df[column].iloc[0] if not df[column].empty else 'N/A'
            missing_values = df[column].isna().sum()
            column_info.append(
                {'name': column, 'first_item': first_item, 'missing': f"{missing_values} missing"})
    except Exception as e:
        flash(f'Error reading file: {e}', 'error')
        return redirect(url_for('select_columns', selected_file=selected_file))

    return render_template('view_worksheet.html', column_info=column_info, selected_file=selected_file,
                           worksheet_name=selected_worksheet, total_values=total_values)


@app.route('/save_processed_data', methods=['POST'])
def save_processed_data():
    selected_columns = request.form.getlist('columns')
    selected_file = request.form.get('selected_file')
    selected_worksheet = request.form.get('selected_worksheet')
    file_path = os.path.join(app.config['DATA_RAW_FOLDER'], selected_file)

    try:
        df = pd.read_excel(file_path, sheet_name=selected_worksheet, usecols=selected_columns)
        processed_file_path = os.path.join(app.config['DATA_PROCESSED_FOLDER'], f"processed_{selected_file}")
        df.to_csv(processed_file_path, index=False)
        flash('File saved successfully', 'success')
    except Exception as e:
        flash(f'Error processing file: {e}', 'error')

    return redirect(url_for('data_management'))


@app.route('/process_selected_columns', methods=['POST'])
def process_selected_columns():
    selected_columns = request.form.getlist('columns')
    selected_file = request.form.get('selected_file')
    file_path = os.path.join(app.config['DATA_RAW_FOLDER'], selected_file)

    try:
        if selected_file.endswith('.csv'):
            df = pd.read_csv(file_path, usecols=selected_columns)
        elif selected_file.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path, usecols=selected_columns)
        else:
            flash('Unsupported file format', 'error')
            return redirect(url_for('data_management'))

        processed_file_name = f"processed_{os.path.splitext(selected_file)[0]}.csv"
        processed_file_path = os.path.join(app.config['DATA_PROCESSED_FOLDER'], processed_file_name)
        df.to_csv(processed_file_path, index=False)
        flash(f'File saved successfully as {processed_file_name}', 'success')

    except Exception as e:
        flash(f'Error processing file: {e}', 'error')
        return redirect(url_for('select_columns', selected_file=selected_file))

    return redirect(url_for('data_management'))
