# app/modules/file_management.py
import os

import openpyxl
import pandas as pd
from flask import current_app
from werkzeug.utils import secure_filename


class FileManagement:
    def __init__(self):
        self.raw_data_dir = current_app.config['RAW_DATA_DIR']
        self.clean_data_dir = current_app.config['CLEAN_DATA_DIR']
        self.processed_data_dir = current_app.config['PROCESSED_DATA_DIR']
        self.allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def _get_directory(self, directory_type):
        if directory_type == 'raw':
            return self.raw_data_dir
        elif directory_type == 'clean':
            return self.clean_data_dir
        elif directory_type == 'processed':
            return self.processed_data_dir
        else:
            raise ValueError("Invalid directory type")

    def list_files(self, directory_type):
        directory = self._get_directory(directory_type)
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        return [f for f in os.listdir(directory) if f.split('.')[-1] in allowed_extensions]

    def upload_file(self, file, directory_type='raw'):
        if not file:
            return 'No file provided'

        if file.filename == '':
            return 'No selected file'

        if not self.allowed_file(file.filename):
            return 'File type not allowed'

        filename = secure_filename(file.filename)
        directory = self._get_directory(directory_type)
        file_path = os.path.join(directory, filename)

        # Check if file already exists
        if os.path.exists(file_path):
            return f'File {filename} already exists in {directory_type} directory'

        try:
            file.save(file_path)
            return f'File {filename} uploaded successfully to {directory_type} directory'
        except Exception as e:
            # Log the exception for debugging purposes
            # For example, you can log to a file or use a logging framework
            print(f"Failed to save file: {e}")
            return 'An error occurred during file upload'

    def delete_file(self, filename, directory_type='raw'):
        try:
            file_path = os.path.join(self._get_directory(directory_type), filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return f'File {filename} deleted successfully'
            else:
                return f'File {filename} does not exist'
        except Exception as e:
            return f'An error occurred: {e}'

    @staticmethod
    def list_worksheets(file_path):
        try:
            if file_path.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(file_path, read_only=True)
                return workbook.sheetnames
            elif file_path.endswith('.xls'):
                # For .xls files, you can use the xlrd library
                pass
            else:
                return 'Unsupported file type for worksheet listing'
        except Exception as e:
            return f'An error occurred: {e}'

    @staticmethod
    def view_csv_contents(file_path, columns=None):
        try:
            df = pd.read_csv(file_path)
            df = df[columns] if columns else df
            return df.head(5).to_html(classes=['table table-noto table-sm'], justify='left', index=False)
        except Exception as e:
            return f'An error occurred: {e}'

    @staticmethod
    def view_spreadsheet_contents(file_path, sheet_name):
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            summary = {
                col: {
                    'column_name': col,
                    'first_item': df[col].iloc[0],
                    'missing_count': df[col].isna().sum()
                } for col in df.columns
            }
            metadata = {'total_rows': len(df), 'worksheet_name': sheet_name}
            return summary, metadata
        except Exception as e:
            return f'An error occurred: {e}', {}

    def save_as_csv(self, df, filename, dir_path, encoding='utf-8'):
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file_path = os.path.join(dir_path, filename)
            df.to_csv(file_path, index=False, encoding=encoding)
            return f'File saved successfully: {file_path}'
        except Exception as e:
            return f'An error occurred: {str(e)}'
