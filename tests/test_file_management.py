from io import StringIO
from unittest.mock import Mock, patch, MagicMock

import pandas
import pandas as pd
import pytest
from flask import Flask
from werkzeug.datastructures import FileStorage

from app.modules.file_management import FileManagement


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.update({
        'RAW_DATA_DIR': '/tmp',
        'CLEAN_DATA_DIR': '/tmp',
        'PROCESSED_DATA_DIR': '/tmp',
        'ALLOWED_EXTENSIONS': {'txt', 'csv'}
    })

    with app.app_context():
        file_management = FileManagement()
        yield app, file_management


def test_allowed_file(app):
    _, file_management = app
    assert file_management.allowed_file('test.txt')
    assert not file_management.allowed_file('test.exe')


def test_upload_file(app):
    _, file_management = app
    mock_file = Mock(spec=FileStorage)
    mock_file.filename = 'test_file.txt'

    with patch('os.path.exists', return_value=False):
        response = file_management.upload_file(mock_file, 'raw')
    assert response == 'File test_file.txt uploaded successfully to raw directory'


def test_delete_file(app):
    _, file_management = app
    with patch('os.path.exists', return_value=True), patch('os.remove'):
        response = file_management.delete_file('test_file.txt', 'raw')
    assert response == 'File test_file.txt deleted successfully'


def test_list_worksheets(app):
    _, file_management = app

    # Mock the workbook object and set sheetnames property
    workbook_mock = MagicMock()
    workbook_mock.sheetnames = ['Sheet1', 'Sheet2']

    with patch('openpyxl.load_workbook', return_value=workbook_mock):
        sheets = file_management.list_worksheets('/tmp/test.xlsx')
    assert sheets == ['Sheet1', 'Sheet2']


def test_view_csv_contents(app):
    _, file_management = app
    csv_data = 'col1,col2\n1,2\n3,4'
    df = pd.read_csv(StringIO(csv_data))

    with patch('pandas.read_csv', return_value=df):
        contents = file_management.view_csv_contents('/tmp/test.csv')
        # Convert DataFrame to HTML string table, your output comparison here may vary
        expected_html = df.head(5).to_html(classes=['table table-noto table-sm'], justify='left', index=False)
    assert contents == expected_html


def test_upload_empty_file(app):
    _, file_management = app
    mock_empty_file = Mock(spec=FileStorage)
    mock_empty_file.filename = ''
    response = file_management.upload_file(mock_empty_file, 'raw')
    assert response == 'No selected file'


def test_upload_disallowed_file_extension(app):
    _, file_management = app
    mock_file = Mock(spec=FileStorage)
    mock_file.filename = 'test.exe'
    response = file_management.upload_file(mock_file, 'raw')
    assert response == 'File type not allowed'


def test_delete_non_existent_file(app):
    _, file_management = app
    with patch('os.path.exists', return_value=False):
        response = file_management.delete_file('test_file.txt', 'raw')
    assert response == 'File test_file.txt does not exist'


def test_list_files_non_existent_directory(app):
    _, file_management = app
    with patch('os.path.exists', return_value=False):
        file_list = file_management.list_files('/non_existent_dir')
    assert file_list == []


def test_list_worksheets_non_excel_file(app):
    _, file_management = app
    response = file_management.list_worksheets('/tmp/test.txt')
    assert response == 'Unsupported file type for worksheet listing'


def test_view_csv_contents_non_csv_file(app):
    _, file_management = app
    with patch('pandas.read_csv', side_effect=pandas.errors.ParserError):
        with pytest.raises(pandas.errors.ParserError):
            pandas.read_csv('/tmp/test.txt')


def test_get_csv_columns_non_existent_file(app):
    _, file_management = app
    with patch('pandas.read_csv', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            pandas.read_csv('/non_existent_dir/test.csv')


def test_get_csv_columns(app):
    _, file_management = app
    csv_data = 'col1,col2\n1,2\n3,4'
    df = pd.read_csv(StringIO(csv_data))

    with patch('pandas.read_csv', return_value=df):
        columns = file_management.get_csv_columns('/tmp/test.csv')
    assert columns == ['col1', 'col2']
