import pytest
from flask import Flask, request
from unittest.mock import MagicMock, patch
from io import BytesIO
from modules.upload import upload_parse_resume, allowed_file


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_allowed_file():
    assert allowed_file("resume.pdf") == True
    assert allowed_file("resume.txt") == False
    assert allowed_file("resume.PDF") == True
    assert allowed_file("resume") == False


@patch('modules.upload.parse_resume', return_value="Parsed resume text")
def test_upload_parse_resume_success(mock_parse_resume, app):
    # Create a mock request
    mock_file = BytesIO(b'This is a test pdf file.')
    mock_file.filename = "resume.pdf"

    mock_request = MagicMock()
    mock_request.files = {'file': mock_file}
    mock_request.form = {'user_id': '123'}

    mock_resume_collection = MagicMock()

    with app.app_context():  # Set up the application context
        response = upload_parse_resume(mock_request, mock_resume_collection)

    assert response[1] == 200
    assert response[0].json['message'] == "File successfully uploaded and parsed"

    mock_resume_collection.insert_one.assert_called_once_with({
        "user_id": '123',
        "resume_text": "Parsed resume text"
    })


@patch('modules.upload.parse_resume', return_value="Parsed resume text")
def test_upload_parse_resume_invalid_format(mock_parse_resume, app):
    mock_file = BytesIO(b'This is a test txt file.')
    mock_file.filename = "resume.txt"

    mock_request = MagicMock()
    mock_request.files = {'file': mock_file}
    mock_request.form = {'user_id': '123'}

    mock_resume_collection = MagicMock()

    with app.app_context():
        response = upload_parse_resume(mock_request, mock_resume_collection)

    assert response[1] == 400
    assert response[0].json['error'] == "Invalid file format, only PDF is allowed"


@patch('modules.upload.parse_resume', return_value="Parsed resume text")
def test_upload_parse_resume_no_file(mock_parse_resume, app):
    mock_request = MagicMock()
    mock_request.files = {}
    mock_request.form = {'user_id': '123'}

    mock_resume_collection = MagicMock()

    with app.app_context():
        response = upload_parse_resume(mock_request, mock_resume_collection)

    assert response[1] == 400
    assert response[0].json['error'] == "No file part in the request"
