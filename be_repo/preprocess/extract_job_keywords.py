"""
This module is responsible for extracting keywords from job descriptions using the OpenAI API.
"""

import json
import os
import pandas as pd
from openai import OpenAI

# Load the OpenAI API key
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)
client = OpenAI(
    api_key=config['CHATGPT_API_KEY']
)


def extract_keywords(csv_file_path, max_rows=100):
    """
    This function reads a CSV file, processes each job description, and extracts
    keywords such as programming languages, technology stacks, soft skills, etc.,
    by calling the OpenAI API. The results are saved to a new CSV file.
    """

    df = pd.read_csv(csv_file_path, index_col=False)
    df = df.drop(columns=df.columns[0])
    df = df.iloc[:max_rows]

    # Keywords
    df['Programming Languages'] = ''
    df['Technology Stacks'] = ''
    df['Soft Skills'] = ''
    df['Work Experience Requirements'] = ''
    df['Educational Requirements'] = ''
    df['Certifications'] = ''
    df['Tools and Software'] = ''
    df['Job Responsibilities'] = ''
    df['Other Domain-Specific Knowledge'] = ''

    for idx, row in df.iterrows():
        text = row['Job Description']

        # Response in JSON format
        prompt = (
            f"Please extract the following information from the job description below in *exact* JSON format with *consistent* field names as follows: \n"
            f"- programming_languages\n"
            f"- technology_stacks\n"
            f"- soft_skills\n"
            f"- work_experience_requirements\n"
            f"- educational_requirements\n"
            f"- certifications\n"
            f"- tools_and_software\n"
            f"- job_responsibilities\n"
            f"- other_domain_specific_knowledge\n\n"
            f"Job description: {text}\n\n"
            f"Return the result in *strict* JSON format with the exact field names as specified above."
        )

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'system',
                       'content': 'You are an expert in analyzing job descriptions and extracting relevant technical skills, programming languages, technologies, and soft skills.'},
                      {'role': 'user', 'content': prompt}],
            max_tokens=500,
            temperature=0.7
        )

        result = response.choices[0].message.content
        result = result.strip().lstrip("```json").rstrip("```")

        try:
            result_dict = json.loads(result)

            print(f"Processing row {idx + 1}")
            print(f"Extracted data: {result_dict}")

            df.at[idx, 'Programming Languages'] = result_dict.get('programming_languages', '')
            df.at[idx, 'Technology Stacks'] = result_dict.get('technology_stacks', '')
            df.at[idx, 'Soft Skills'] = result_dict.get('soft_skills', '')
            df.at[idx, 'Work Experience Requirements'] = result_dict.get('work_experience_requirements', '')
            df.at[idx, 'Educational Requirements'] = result_dict.get('educational_requirements', '')
            df.at[idx, 'Certifications'] = result_dict.get('certifications', '')
            df.at[idx, 'Tools and Software'] = result_dict.get('tools_and_software', '')
            df.at[idx, 'Job Responsibilities'] = result_dict.get('job_responsibilities', '')
            df.at[idx, 'Other Domain-Specific Knowledge'] = result_dict.get('other_domain_specific_knowledge', '')

        except Exception as e:
            print(f"Error parsing response for row {idx}: {e}")
            continue

    output_file = csv_file_path.replace('.csv', '_with_keywords.csv')
    df.to_csv(output_file, index=False)
    print(f'Keywords extracted and saved to {output_file}')


import pandas as pd
from collections import Counter


def clean_and_split(column_value):
    """
    Clean unwanted characters from the string, split it by ', ', and remove empty strings.

    Args:
        column_value (str): The string value to clean, split, and remove empty items.

    Returns:
        list: A list of cleaned, split items without empty strings.
    """
    if pd.isna(column_value):
        return []

    # Remove unwanted characters like '[', ']', and single quotes
    cleaned_value = column_value.replace('[', '').replace(']', '').replace("'", '')

    # Split by ', ' and remove empty strings from the resulting list
    return [item.strip() for item in cleaned_value.split(', ') if item.strip()]


def find_all_skills_with_counts(df):
    """
    Find and count all Programming Languages, Technology Stacks, and Tools and Software for each Job Title.
    Output them in a format such as 'Java-13, Node.js-5, PHP-3' sorted by count.

    Args:
        df (pd.DataFrame): The DataFrame containing Job Titles and the corresponding extracted keywords.

    Returns:
        pd.DataFrame: A summary DataFrame containing all skills and their counts for each Job Title.
    """

    # Define the columns to aggregate
    columns_to_summarize = ['Programming Languages', 'Technology Stacks', 'Tools and Software']

    # Initialize an empty list to store the results
    summary_list = []

    # Group the DataFrame by Job Title
    grouped = df.groupby('Job Title')

    for job_title, group in grouped:
        # Initialize dictionaries to store aggregated data
        programming_langs_counter = Counter()
        tech_stacks_counter = Counter()
        tools_counter = Counter()

        # Iterate through the group to aggregate the relevant columns
        for _, row in group.iterrows():
            # Clean, split, and remove empty values
            programming_langs_counter.update(clean_and_split(row['Programming Languages']))
            tech_stacks_counter.update(clean_and_split(row['Technology Stacks']))
            tools_counter.update(clean_and_split(row['Tools and Software']))

        # Format the counts as 'Item-Count', sorted by count in descending order
        core_programming_langs = ', '.join(
            [f'{item}-{count}' for item, count in programming_langs_counter.most_common()])
        core_tech_stacks = ', '.join([f'{item}-{count}' for item, count in tech_stacks_counter.most_common()])
        core_tools = ', '.join([f'{item}-{count}' for item, count in tools_counter.most_common()])

        # Append the results for this job title
        summary_list.append({
            'Job Title': job_title,
            'Programming Languages (Count)': core_programming_langs,
            'Technology Stacks (Count)': core_tech_stacks,
            'Tools and Software (Count)': core_tools
        })

    # Convert the summary list to a DataFrame
    summary_df = pd.DataFrame(summary_list)

    return summary_df




if __name__ == '__main__':
    csv_file = 'job_title_des.csv'
    # extract_keywords(csv_file)


    # Assuming df contains the Job Title, Programming Languages, Technology Stacks, Tools and Software
    df = pd.read_csv('job_title_des_with_keywords.csv')

    # Call the function to summarize core skills for each Job Title
    core_skills_df = find_all_skills_with_counts(df)

    # Save the result to a new CSV file
    core_skills_df.to_csv('core_skills_summary.csv', index=False)

    print('Core skills for each Job Title saved to core_skills_summary.csv')