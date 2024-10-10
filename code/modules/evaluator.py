"""
This module is responsible for evaluating resumes based on specified criteria.
"""

import json
import os
from openai import OpenAI

# Load the OpenAI API key
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)
client = OpenAI(
    api_key=config['CHATGPT_API_KEY']
)

# Define the scoring criteria and weights
SCORING_CRITERIA = {
    'Relevance of Job Description': 30,
    'Achievements and Impact': 25,
    'Education and Certifications': 15,
    'Resume Structure and Presentation': 10,
    'Soft Skills': 10,
    'Consistency and Chronology': 10
}


def evaluate_resume(resume_text):
    """
    Evaluate resumes by calling ChatGPT API
    """
    try:
        prompt = f"""
        Please evaluate the following resume based on the criteria below, and structure your response according to the format provided:

        Criteria:
        1. Relevance of Job Description (30%)
        2. Achievements and Impact (25%)
        3. Education and Certifications (15%)
        4. Resume Structure and Presentation (10%)
        5. Soft Skills (10%)
        6. Consistency and Chronology (10%)

        The response should follow this format:

        ### Scores for each criteria:
        1. Relevance of Job Description: X/100
        2. Achievements and Impact: X/100
        3. Education and Certifications: X/100
        4. Resume Structure and Presentation: X/100
        5. Soft Skills: X/100
        6. Consistency and Chronology: X/100

        ### Weighted Total Score: Y/100

        ### Explanation for each criteria:
        1. Relevance of Job Description:
        [Explanation of the score]
        2. Achievements and Impact:
        [Explanation of the score]
        3. Education and Certifications:
        [Explanation of the score]
        4. Resume Structure and Presentation:
        [Explanation of the score]
        5. Soft Skills:
        [Explanation of the score]
        6. Consistency and Chronology:
        [Explanation of the score]

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
        return evaluation

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
