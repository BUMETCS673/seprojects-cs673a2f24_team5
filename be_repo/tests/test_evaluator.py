import pytest
import json
from unittest.mock import MagicMock, patch
from configs.openai_client import get_openai_client
from modules.evaluator import evaluate_resume, extract_keywords, evaluate_resume_with_jd


@pytest.fixture
def mock_openai_client():
    client = MagicMock()
    get_openai_client.return_value = client
    return client


def test_evaluate_resume(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value.choices[0].message.content = '''{
        "scores": {
            "Education": 18,
            "Project and Work Experience": 25,
            "Skills and Certifications": 28,
            "Soft Skills": 8,
            "Resume Structure and Presentation": 4,
            "Consistency and Chronology": 4
        },
        "weighted_total_score": 87,
        "explanations": {
            "Education": {
                "score": 18,
                "explanation": "Good education background with relevant degree."
            },
            "Project and Work Experience": {
                "score": 25,
                "explanation": "Sufficient experience but lacks variety."
            },
            "Skills and Certifications": {
                "score": 28,
                "explanation": "Highly skilled in the relevant areas."
            },
            "Soft Skills": {
                "score": 8,
                "explanation": "Good communication skills."
            },
            "Resume Structure and Presentation": {
                "score": 4,
                "explanation": "Well-structured resume."
            },
            "Consistency and Chronology": {
                "score": 4,
                "explanation": "Consistent and in chronological order."
            }
        }
    }'''

    resume_text = "Sample resume text"
    evaluation = evaluate_resume(resume_text)
    assert evaluation['scores']['Education'] >= 0
    assert evaluation['weighted_total_score'] >= 0


def test_extract_keywords(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value.choices[0].message.content = '''{
        "Education": ["Bachelor's Degree in Computer Science"],
        "Project and Work Experience": ["Software development", "Machine learning"],
        "Skills and Certifications": ["Python", "AWS Certification"],
        "Soft Skills": ["Leadership", "Teamwork"]
    }'''

    text = "Sample resume text"
    keywords = extract_keywords(text)
    keywords_json = json.loads(keywords)
    assert "Education" in keywords_json
    assert "Skills and Certifications" in keywords_json


def test_evaluate_resume_with_jd(mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='''{
            "Education": ["Bachelor's Degree in Computer Science"],
            "Project and Work Experience": ["Software development", "Machine learning"],
            "Skills and Certifications": ["Python", "AWS Certification"],
            "Soft Skills": ["Leadership", "Teamwork"]
        }'''))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='''{
            "correlation": {
                "Education": 0.8,
                "Project and Work Experience": 0.7,
                "Skills and Certifications": 0.9,
                "Soft Skills": 0.6
            },
            "explanations": {
                "Education": {
                    "explanation": "Relevant education background."
                },
                "Project and Work Experience": {
                    "explanation": "Good experience in the relevant field."
                },
                "Skills and Certifications": {
                    "explanation": "Excellent skillset matching the requirements."
                },
                "Soft Skills": {
                    "explanation": "Soft skills partially align with the requirements."
                }
            }
        }'''))])
    ]

    resume_text = "Sample resume text"
    jd_text = "Sample job description"
    evaluation_with_jd = evaluate_resume_with_jd(resume_text, jd_text)
    assert evaluation_with_jd['scores']['Education'] >= 0
    assert "explanations" in evaluation_with_jd
