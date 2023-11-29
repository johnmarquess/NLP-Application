import io
import os

import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Description of Data Modeling' in response.data


def test_file_upload(client):
    data = {
        'file': (io.BytesIO(b'my file contents'), 'test.xlsx'),
    }
    response = client.post('/data-management', data=data, content_type='multipart/form-data')
    assert response.status_code == 200


def test_select_file(client):
    test_file_name = 'test_file.xlsx'
    data = {'selected_file': test_file_name}
    response = client.post('/select-file', data=data, follow_redirects=True)
    # Check if the response is correct
    assert response.status_code == 200


def test_worksheet_selection(client):
    test_file_name = 'test_file.xlsx'
    test_sheet_name = 'Sheet1'

    # Select the file first
    response = client.post('/select-worksheet', data={
        'selected_file': test_file_name,
        'selected_sheet': test_sheet_name
    }, follow_redirects=True)

    assert response.status_code == 200
    assert test_sheet_name.encode() in response.data  # Check if the response contains the sheet name


def test_save_csv(client, app):
    with app.app_context():  # Set up test data
        test_file_name = 'test_file.xlsx'
        test_sheet_name = 'Sheet1'
        test_csv_name = 'test_file'
        test_columns = ['col1', 'col2']

        # Prepare the data for POST request
        data = {
            'selected_file': test_file_name,
            'selected_sheet': test_sheet_name,
            'selected_columns': test_columns,
            'csv_name': test_csv_name
        }

        # Send POST request
        response = client.post('/save-csv', data=data, follow_redirects=True)

        # Check for successful response
        assert response.status_code == 200

        # Verify CSV file existence and content
        csv_path = os.path.join('app', app.config['DATA_SAVED'], test_csv_name + '.csv')
        assert os.path.exists(csv_path)

        # Optionally, read the CSV file and verify its contents
        with open(csv_path, 'r') as f:
            content = f.read()
            # Perform assertions on the content, like checking for specific data
            assert 'col1' in content
            assert 'col2' in content
            assert 'col3' not in content

