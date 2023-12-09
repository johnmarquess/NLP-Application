from unittest.mock import patch

import pandas as pd
import pytest

from app import create_app

# Instance of Flask web server
flask_app = create_app()
app = flask_app.test_client()
app.testing = True

# create a sample dataframe that will be returned by the mock
sample_data = {'column1': ['value1', 'value2', 'value3'],
               'column2': ['value4', 'value5', 'value6']}
sample_df = pd.DataFrame(sample_data)


@pytest.fixture
def client():
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


def test_get_files(client):
    rv = client.get('/get-files')  # direct string instead of url_for
    assert rv.status_code == 200


def test_file_manager(client):
    rv = client.get('/file-manager')
    assert rv.status_code == 200

    rv = client.post('/file-manager')
    assert rv.status_code == 200

    rv = client.post('/file-manager', data={'file': 'test_file.txt'})
    assert rv.status_code == 200

    rv = client.post('/file-manager', data={'file': 'test_file.txt', 'submit': 'Upload'})
    assert rv.status_code == 200


def test_view_worksheet(client):
    # QUERY_STRING is used to add request parameters to the URL
    rv = client.get('/view-worksheet', query_string={"file_path": "YOUR_FILE_PATH", "sheet_name": "SHEET_NAME"})
    assert rv.status_code == 200


@pytest.fixture
def client(monkeypatch):
    # This function will be used to replace pd.read_excel
    def mock_read_excel(*args, **kwargs):
        return sample_df

    monkeypatch.setattr('pandas.read_excel', mock_read_excel)
    # With the monkeypatch fixture, you don't need to use 'with'

    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


def mock_delete_file(file_path):
    pass


@patch('app.modules.file_management.FileManagement.delete_file', new=mock_delete_file)
def test_delete_file(client):
    rv = client.post('/delete-file/raw', data={"file": "test_file.txt"})
    print(rv.data)  # print the response to inspect its content
    assert rv.status_code == 302


