"""
Flask Integration Test.
"""
import pytest
from flask import Flask
from app import app
from configs.database import get_resume_database


@pytest.fixture
def client():
    # Create testing client
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    client = app.test_client()

    with app.app_context():
        database = get_resume_database()
        resume_collection = database.get_collection("resumes")
        resume_collection.delete_many({"user_id": "test"})
        yield client, resume_collection
        resume_collection.delete_many({"user_id": "test"})


def test_resume_evaluate(client):
    client, resume_collection = client

    resume_collection.insert_one({
        'user_id': 'test',
        'resume_text': 'Sample resume content for evaluation.'
    })

    response = client.post('/resume_evaluate', data={'user_id': 'test'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'analysis' in json_data


def test_resume_evaluate_with_JD(client):
    client, resume_collection = client

    resume_collection.insert_one({
        'user_id': 'test',
        'resume_text': 'Sample resume content for JD evaluation.'
    })

    response = client.post('/resume_evaluate_with_JD', data={
        'user_id': 'test',
        'jd_text': 'Sample job description text for matching.'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'analysis' in json_data
