"""
This module is responsible for evaluating resumes based on specified criteria.
"""

import json
from configs.openai_client import get_openai_client

# Define the scoring criteria and weights
SCORING_CRITERIA = {
    'Education': 20,
    'Project and Work Experience': 30,
    'Skills and Certifications': 30,
    'Soft Skills': 10,
    'Resume Structure and Presentation': 5,
    'Consistency and Chronology': 5
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
        1. Education (20%)
        2. Project and Work Experience (30%)
        3. Skills and Certifications(30%)
        4. Soft Skills (10%)
        5. Resume Structure and Presentation (5%)
        6. Consistency and Chronology (5%)

        The response should be in the following JSON format:

        {{
            "scores": {{
                "Education": X,
                "Project and Work Experience": X,
                "Skills and Certifications": X,
                "Soft Skills": X,
                "Resume Structure and Presentation": X,
                "Consistency and Chronology": X
            }},
            "weighted_total_score": Y,
            "explanations": {{
                "Education": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Project and Work Experience": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Skills and Certifications": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Soft Skills": {{
                    "score": X,
                    "explanation": "[Explanation of the score]"
                }},
                "Resume Structure and Presentation": {{
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
    scores['Education'] = int(lines[1].split(':')[1].strip().replace('/100', ''))
    scores['Project and Work Experience'] = int(lines[2].split(':')[1].strip().replace('/100', ''))
    scores['Skills and Certifications'] = int(lines[3].split(':')[1].strip().replace('/100', ''))
    scores['Soft Skills'] = int(lines[4].split(':')[1].strip().replace('/100', ''))
    scores['Resume Structure and Presentation'] = int(lines[5].split(':')[1].strip().replace('/100', ''))
    scores['Consistency and Chronology'] = int(lines[6].split(':')[1].strip().replace('/100', ''))

    # Weighted total score
    weighted_score = float(lines[8].split(':')[1].strip().replace('/100', ''))

    # Explanation part
    explanation = '\n'.join(lines[11:])

    return scores, weighted_score, explanation


def compute_correlated_score(score, correlation):
    max_ranges = [SCORING_CRITERIA['Education'], SCORING_CRITERIA['Project and Work Experience'],
                  SCORING_CRITERIA['Skills and Certifications'], SCORING_CRITERIA['Soft Skills']]
    correlated_score = [min(int(score[i] * correlation[i] ** 2 * 2), max_ranges[i]) for i in range(4)]

    return correlated_score


def extract_keywords(text):
    """
    Extracts keywords from resume and jd.
    """
    prompt = (
        f"Please extract the following information **only using keywords** from the MYTEXT below. "
        f"Ensure the output is in *exact* JSON format, and each field only contains relevant keywords "
        f"(single words or short phrases) with *consistent* field names as follows:\n"
        f"- Education (e.g., degrees, fields of study, universities)\n"
        f"- Project and Work Experience (e.g., technologies, tools, project types, roles)\n"
        f"- Skills and Certifications (e.g., programming languages, certifications)\n"
        f"- Soft Skills (e.g., leadership, communication, teamwork)\n"
        f"MYTEXT: {text}\n\n"
        f"Return the result in the following *strict* JSON format:\n"
        f"{{\n"
        f'  "Education": ["keyword1", "keyword2", ...],\n'
        f'  "Project and Work Experience": ["keyword1", "keyword2", ...],\n'
        f'  "Skills and Certifications": ["keyword1", "keyword2", ...],\n'
        f'  "Soft Skills": ["keyword1", "keyword2", ...]\n'
        f"}}"
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'system',
                   'content': 'You are an expert in analyzing resumes and job descriptions and extracting relevant education, project and work experience, skills, and soft skills.'},
                  {'role': 'user', 'content': prompt}],
        max_tokens=500,
        temperature=0.7
    )

    result = response.choices[0].message.content
    result = result.strip().lstrip("```json").rstrip("```")

    return result


def evaluate_resume_with_jd(resume_text, jd_text):
    """
    Evaluate resume with jd, compute the correlation between resume and jd
    """
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    prompt = (
        f"Based on the given resume keywords and job description keywords, "
        f"analyze the **correlation** between them. Focus on the following four fields:\n"
        f"- Education\n"
        f"- Project and Work Experience\n"
        f"- Skills and Certifications\n"
        f"- Soft Skills\n\n"
        f"For each field, evaluate the **degree of matching** between the resume and job description keywords, "
        f"and provide a correlation score between **0 and 1** (one decimal place), "
        f"where 1 means a perfect match and 0 means no match.\n\n"
        f"In addition, provide an explanation for each field describing only the reasons for the alignment or lack thereof. "
        f"Do not mention the correlation score in the explanation, just provide the reasons.\n\n"
        f"Return the result in the following *strict JSON format*:\n"
        f"{{\n"
        f'  "correlation": {{\n'
        f'    "Education": 0.0,\n'
        f'    "Project and Work Experience": 0.0,\n'
        f'    "Skills and Certifications": 0.0,\n'
        f'    "Soft Skills": 0.0\n'
        f'  }},\n'
        f'  "explanations": {{\n'
        f'    "Education": {{\n'
        f'      "explanation": "Describe the alignment or lack of alignment with education requirements without mentioning scores."\n'
        f'    }},\n'
        f'    "Project and Work Experience": {{\n'
        f'      "explanation": "Provide details on the work experience relevance without mentioning scores."\n'
        f'    }},\n'
        f'    "Skills and Certifications": {{\n'
        f'      "explanation": "Explain the relevance of skills and certifications without mentioning scores."\n'
        f'    }},\n'
        f'    "Soft Skills": {{\n'
        f'      "explanation": "Indicate how the resume reflects soft skills without mentioning scores."\n'
        f'    }}\n'
        f'  }}\n'
        f"}}\n\n"
        f"resume_keywords: {resume_keywords}\n\n"
        f"job_description_keywords: {jd_keywords}\n\n"
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{
            'role': 'system',
            'content': (
                'You are an expert in analyzing and comparing resumes with job descriptions. '
                'Your task is to evaluate how well the resume matches the job description in key technical and soft skill areas.'
            )
        },
            {'role': 'user', 'content': prompt}],
        max_tokens=500,
        temperature=0.7
    )

    correlation = response.choices[0].message.content
    correlation = correlation.strip().lstrip("```json").rstrip("```")
    correlation = json.loads(correlation)

    evaluated_resume_with_jd = evaluate_resume(resume_text)

    # Extract correlation scores and original scores into arrays and compute correlated_score
    correlation_array = list(correlation['correlation'].values())
    scores_array = list(evaluated_resume_with_jd['scores'].values())
    correlated_score = compute_correlated_score(scores_array, correlation_array)

    # Update the scores and explanations in the evaluated resume based on correlation analysis
    fields_to_replace = ['Education', 'Project and Work Experience', 'Skills and Certifications', 'Soft Skills']

    for i, field in enumerate(fields_to_replace):
        evaluated_resume_with_jd['scores'][field] = correlated_score[i]
        evaluated_resume_with_jd['explanations'][field]['score'] = correlated_score[i]
        evaluated_resume_with_jd['explanations'][field]['explanation'] = correlation['explanations'][field][
            'explanation']

    evaluated_resume_with_jd['weighted_total_score'] = sum(evaluated_resume_with_jd['scores'].values())

    return evaluated_resume_with_jd
