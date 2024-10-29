"""
This module is responsible for evaluating resumes based on specified criteria.
"""

import json
from configs.openai_client import get_openai_client

# Define the scoring criteria and weights
SCORING_CRITERIA = {
    'Relevance of Job Description': 30,
    'Achievements and Impact': 25,
    'Education and Certifications': 15,
    'Resume Structure and Presentation': 10,
    'Soft Skills': 10,
    'Consistency and Chronology': 10
}

client = get_openai_client()


def evaluate_resume(resume_text):
    """
    Evaluate resumes by calling ChatGPT API
    """
    try:
        prompt = f"""
        Please evaluate the following resume based on the criteria below, and structure your response in JSON format:

        Criteria:
        1. Relevance of Job Description (30%)
        2. Achievements and Impact (25%)
        3. Education and Certifications (15%)
        4. Resume Structure and Presentation (10%)
        5. Soft Skills (10%)
        6. Consistency and Chronology (10%)

        The response should be in the following JSON format:

        {{
            "scores": {{
                "Relevance of Job Description": X,
                "Achievements and Impact": X,
                "Education and Certifications": X,
                "Resume Structure and Presentation": X,
                "Soft Skills": X,
                "Consistency and Chronology": X
            }},
            "weighted_total_score": Y,
            "explanations": {{
                "Relevance of Job Description": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Achievements and Impact": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Education and Certifications": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Resume Structure and Presentation": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Soft Skills": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Consistency and Chronology": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }}
            }}
        }}

        Resume: {resume_text}
        """

        # Call the evaluation API
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'system', 'content': 'You are a professional resume evaluator.'},
                      {'role': 'user', 'content': prompt}],
            max_tokens=500,
            temperature=0.7
        )

        evaluation = response.choices[0].message.content
        evaluation = evaluation.strip().lstrip("```json").rstrip("```")

        # Return the JSON formatted evaluation
        evaluation_json = json.loads(evaluation)
        return evaluation_json

    except Exception as e:
        return f'Error evaluating resume: {str(e)}'


def extract_scores_and_explanation(evaluation):
    """
    Extracts the scores and explanations from the evaluation response.
    """
    scores = {}
    explanation = ''
    lines = evaluation.split('\n')

    # 6 criteria scores
    scores['Relevance of Job Description'] = int(lines[1].split(':')[1].strip().replace('/100', ''))
    scores['Achievements and Impact'] = int(lines[2].split(':')[1].strip().replace('/100', ''))
    scores['Education and Certifications'] = int(lines[3].split(':')[1].strip().replace('/100', ''))
    scores['Resume Structure and Presentation'] = int(lines[4].split(':')[1].strip().replace('/100', ''))
    scores['Soft Skills'] = int(lines[5].split(':')[1].strip().replace('/100', ''))
    scores['Consistency and Chronology'] = int(lines[6].split(':')[1].strip().replace('/100', ''))

    # Weighted total score
    weighted_score = float(lines[8].split(':')[1].strip().replace('/100', ''))

    # Explanation part
    explanation = '\n'.join(lines[11:])

    return scores, weighted_score, explanation
