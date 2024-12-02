import pandas as pd
import openai
import json
import csv
import os
import re
import time

# Initialize the OpenAI API client
from configs.openai_client import get_openai_client

client = get_openai_client()

# Load your dataset
data = pd.read_csv('resume_job_description_fit_train.csv')

# Create a directory for storing debug responses
debug_dir = 'debug_responses'
os.makedirs(debug_dir, exist_ok=True)

# Define the node types and attributes (with shorter names)
node_types = {
    'Edu': ['id', 'deg', 'f_study', 'inst', 's_year', 'e_year', 'gpa'],
    'WE': ['id', 'pos', 'comp', 'loc'],
    'Proj': ['id', 'ttl', 'desc', 'tech', 'role'],
    'Skill': ['id', 'name'],
    'Cert': ['id', 'name', 'issuer', 'exp'],
    'SSkill': ['id', 'name'],
    'JD': ['id', 'comp', 'req', 'resp', 'loc'],
    'JTitle': ['id', 'ttl', 'lvl', 'cat'],
    'JKeyword': ['id', 'keyword'],
    'Indus': ['id', 'name'],
}

relationships = [
    {'type': 'UTILIZES_SKILL', 'start_node': 'WE', 'end_node': 'Skill'},
    {'type': 'USES_TECH', 'start_node': 'Proj', 'end_node': 'Skill'},
    {'type': 'REL_TO', 'start_node': 'Proj', 'end_node': 'Skill'},
    {'type': 'DESCRIBES', 'start_node': 'JD', 'end_node': 'JTitle'},
    {'type': 'REQ_SKILL', 'start_node': 'JTitle', 'end_node': 'Skill'},
    {'type': 'ASSOC_WITH', 'start_node': 'JTitle', 'end_node': 'JKeyword'},
    {'type': 'MENTIONS', 'start_node': 'JD', 'end_node': 'JKeyword'},
    {'type': 'REQ_EDU', 'start_node': 'JD', 'end_node': 'Edu'},
    {'type': 'DESIRES_SSKILL', 'start_node': 'JD', 'end_node': 'SSkill'},
    {'type': 'BELONGS_TO_INDUS', 'start_node': 'JTitle', 'end_node': 'Indus'},
    {'type': 'REL_TO', 'start_node': 'Skill', 'end_node': 'Skill'},
    {'type': 'REQ_CERT', 'start_node': 'JTitle', 'end_node': 'Cert'},
    {'type': 'BELONGS_TO_INDUS', 'start_node': 'JD', 'end_node': 'Indus'},
    {'type': 'IN_INDUS', 'start_node': 'WE', 'end_node': 'Indus'},
    {'type': 'REL_TO', 'start_node': 'Cert', 'end_node': 'Skill'},
    {'type': 'SIMILAR_TO', 'start_node': 'JKeyword', 'end_node': 'JKeyword'},
    {'type': 'SIMILAR_TO', 'start_node': 'Skill', 'end_node': 'Skill'},
]

# Initialize dictionaries to store nodes and relationships
node_id_counter = 1  # Global counter for node IDs
node_mappings = {node_type: {} for node_type in node_types}

# Initialize relationships data list
relationships_data = []

# Create output directory if not exists
output_dir = 'neo4j_csv'
os.makedirs(output_dir, exist_ok=True)

# Initialize CSV writers for nodes
node_files = {}
node_writers = {}

for node_type, attributes in node_types.items():
    file_path = os.path.join(output_dir, f'{node_type}.csv')
    node_file = open(file_path, 'w', newline='', encoding='utf-8')
    node_writer = csv.DictWriter(node_file, fieldnames=attributes)
    node_writer.writeheader()
    node_files[node_type] = node_file
    node_writers[node_type] = node_writer

# Initialize CSV writer for relationships
relationship_keys = ['start_node_id', 'relationship_type', 'end_node_id']
relationships_file = open(os.path.join(output_dir, 'relationships.csv'), 'w', newline='', encoding='utf-8')
relationships_writer = csv.DictWriter(relationships_file, fieldnames=relationship_keys)
relationships_writer.writeheader()

def generate_prompt(resume_text, job_description_text):
    prompt = f"""
Extract entities and relationships from the following resume and job description.

Your task is to extract both **entities** and **relationships** from the provided texts.

**Valid Relationship Types:**

- **UTILIZES_SKILL:** A Work Experience (`WE`) node **utilizes** a Skill (`Skill`) node. For example, a person used Python during their job at a company.

- **USES_TECH:** A Project (`Proj`) node **uses** a Skill (`Skill`) node as a technology. For example, a project implemented using React.js.

- **REL_TO (Proj to Skill):** A Project (`Proj`) node is **related to** a Skill (`Skill`) node, indicating relevance or association.

- **DESCRIBES:** A Job Description (`JD`) node **describes** a Job Title (`JTitle`) node, providing details about the role.

- **REQ_SKILL:** A Job Title (`JTitle`) node **requires** a Skill (`Skill`) node. The skill is necessary for the job position.

- **ASSOC_WITH:** A Job Title (`JTitle`) node is **associated with** a Job Keyword (`JKeyword`) node, linking keywords relevant to the job.

- **MENTIONS:** A Job Description (`JD`) node **mentions** a Job Keyword (`JKeyword`) node. The keyword appears in the job description.

- **REQ_EDU:** A Job Description (`JD`) node **requires** an Education (`Edu`) node, such as a degree or certification.

- **DESIRES_SSKILL:** A Job Description (`JD`) node **desires** a Soft Skill (`SSkill`) node, indicating preferred soft skills.

- **BELONGS_TO_INDUS (JTitle to Indus):** A Job Title (`JTitle`) node **belongs to** an Industry (`Indus`) node, specifying the industry category.

- **REL_TO (Skill to Skill):** A Skill (`Skill`) node is **related to** another Skill (`Skill`) node, indicating similarity or complementarity.

- **REQ_CERT:** A Job Title (`JTitle`) node **requires** a Certification (`Cert`) node. The certification is needed for the role.

- **BELONGS_TO_INDUS (JD to Indus):** A Job Description (`JD`) node **belongs to** an Industry (`Indus`) node, providing industry context.

- **IN_INDUS:** A Work Experience (`WE`) node is **in** an Industry (`Indus`) node, indicating the industry of the work experience.

- **REL_TO (Cert to Skill):** A Certification (`Cert`) node is **related to** a Skill (`Skill`) node, showing the skill validated by the certification.

- **SIMILAR_TO (JKeyword to JKeyword):** A Job Keyword (`JKeyword`) node is **similar to** another Job Keyword (`JKeyword`) node, indicating related concepts.

- **SIMILAR_TO (Skill to Skill):** A Skill (`Skill`) node is **similar to** another Skill (`Skill`) node, suggesting related skills.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description_text}
\"\"\"

Remember to reference nodes using their `id` fields in the relationships, return the data in the following JSON format without additional explanations:

{{  
    ""nodes"": {{
        ""Edu"": [
            {{
                ""id"": ""edu1"",
                ""deg"": ""Bachelor of Science"",
                ""f_study"": ""Computer Science"",
                ""inst"": ""XYZ University"",
                ""s_year"": ""2010"",
                ""e_year"": ""2014"",
                ""gpa"": ""3.8""
            }}
        ],
        ""WE"": [
            {{
                ""id"": ""we1"",
                ""pos"": ""Data Analyst"",
                ""comp"": ""Tech Solutions Inc"",
                ""loc"": ""San Francisco""
            }}
        ],
        ""Proj"": [
            {{
                ""id"": ""proj1"",
                ""ttl"": ""Data Migration Project"",
                ""desc"": ""Migrated data from legacy systems to cloud"",
                ""tech"": ""AWS, Python"",
                ""role"": ""Lead Developer""
            }}
        ],
        ""Skill"": [
            {{
                ""id"": ""skill1"",
                ""name"": ""SQL""
            }},
            {{
                ""id"": ""skill2"",
                ""name"": ""Python""
            }},
            {{
                ""id"": ""skill3"",
                ""name"": ""Data Modeling""
            }},
            {{
                ""id"": ""skill4"",
                ""name"": ""ETL""
            }}
        ],
        ""Cert"": [
            {{
                ""id"": ""cert1"",
                ""name"": ""AWS Certified Solutions Architect"",
                ""issuer"": ""Amazon"",
                ""exp"": ""2023""
            }}
        ],
        ""SSkill"": [
            {{
                ""id"": ""sskill1"",
                ""name"": ""Team Leadership""
            }}
        ],
        ""JD"": {{
            ""id"": ""jd1"",
            ""comp"": ""ABC Corp"",
            ""req"": ""Experience in Python, SQL, and data analysis"",
            ""resp"": ""Manage data integration projects"",
            ""loc"": ""New York""
        }},
        ""JTitle"": {{
            ""id"": ""jtitle1"",
            ""ttl"": ""Data Engineer"",
            ""lvl"": ""Mid"",
            ""cat"": ""Engineering""
        }},
        ""JKeyword"": [
            {{
                ""id"": ""jkeyword1"",
                ""keyword"": ""Big Data""
            }}
        ],
        ""Indus"": [
            {{
                ""id"": ""indus1"",
                ""name"": ""Information Technology""
            }}
        ]
    }},
    ""rels"": [
        {{
            ""s_type"": ""WE"",
            ""s_id"": ""we1"",
            ""rel"": ""UTILIZES_SKILL"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill1""
        }},
        {{
            ""s_type"": ""Proj"",
            ""s_id"": ""proj1"",
            ""rel"": ""USES_TECH"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill2""
        }},
        {{
            ""s_type"": ""Proj"",
            ""s_id"": ""proj1"",
            ""rel"": ""REL_TO"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill3""
        }},
        {{
            ""s_type"": ""JD"",
            ""s_id"": ""jd1"",
            ""rel"": ""DESCRIBES"",
            ""e_type"": ""JTitle"",
            ""e_id"": ""jtitle1""
        }},
        {{
            ""s_type"": ""JTitle"",
            ""s_id"": ""jtitle1"",
            ""rel"": ""REQ_SKILL"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill2""
        }},
        {{
            ""s_type"": ""JTitle"",
            ""s_id"": ""jtitle1"",
            ""rel"": ""ASSOC_WITH"",
            ""e_type"": ""JKeyword"",
            ""e_id"": ""jkeyword1""
        }},
        {{
            ""s_type"": ""JD"",
            ""s_id"": ""jd1"",
            ""rel"": ""MENTIONS"",
            ""e_type"": ""JKeyword"",
            ""e_id"": ""jkeyword1""
        }},
        {{
            ""s_type"": ""JD"",
            ""s_id"": ""jd1"",
            ""rel"": ""REQ_EDU"",
            ""e_type"": ""Edu"",
            ""e_id"": ""edu1""
        }},
        {{
            ""s_type"": ""JD"",
            ""s_id"": ""jd1"",
            ""rel"": ""DESIRES_SSKILL"",
            ""e_type"": ""SSkill"",
            ""e_id"": ""sskill1""
        }},
        {{
            ""s_type"": ""JTitle"",
            ""s_id"": ""jtitle1"",
            ""rel"": ""BELONGS_TO_INDUS"",
            ""e_type"": ""Indus"",
            ""e_id"": ""indus1""
        }},
        {{
            ""s_type"": ""Skill"",
            ""s_id"": ""skill3"",
            ""rel"": ""REL_TO"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill4""
        }},
        {{
            ""s_type"": ""JTitle"",
            ""s_id"": ""jtitle1"",
            ""rel"": ""REQ_CERT"",
            ""e_type"": ""Cert"",
            ""e_id"": ""cert1""
        }},
        {{
            ""s_type"": ""JD"",
            ""s_id"": ""jd1"",
            ""rel"": ""BELONGS_TO_INDUS"",
            ""e_type"": ""Indus"",
            ""e_id"": ""indus1""
        }},
        {{
            ""s_type"": ""WE"",
            ""s_id"": ""we1"",
            ""rel"": ""IN_INDUS"",
            ""e_type"": ""Indus"",
            ""e_id"": ""indus1""
        }},
        {{
            ""s_type"": ""Cert"",
            ""s_id"": ""cert1"",
            ""rel"": ""REL_TO"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill4""
        }},
        {{
            ""s_type"": ""JKeyword"",
            ""s_id"": ""jkeyword1"",
            ""rel"": ""SIMILAR_TO"",
            ""e_type"": ""JKeyword"",
            ""e_id"": ""jkeyword1""
        }},
        {{
            ""s_type"": ""Skill"",
            ""s_id"": ""skill1"",
            ""rel"": ""SIMILAR_TO"",
            ""e_type"": ""Skill"",
            ""e_id"": ""skill68""
        }}
    ]
}}

"""
    return prompt


function_schema = [
    {
        "name": "extract_entities_and_relationships",
        "description": "Extract entities and relationships from resume and job description.",
        "parameters": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "object",
                    "properties": {
                        "Edu": {  # Education
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "deg": {"type": "string"},           # degree
                                    "f_study": {"type": "string"},       # field_of_study
                                    "inst": {"type": "string"},          # institution
                                    "s_year": {"type": "string"},        # start_year
                                    "e_year": {"type": "string"},        # end_year
                                    "gpa": {"type": "string"},           # GPA
                                },
                                "required": ["id", "deg", "inst"]
                            },
                        },
                        "WE": {  # WorkExperience
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "pos": {"type": "string"},           # position
                                    "comp": {"type": "string"},          # company
                                    "loc": {"type": "string"},           # location
                                },
                                "required": ["id", "pos", "comp"]
                            },
                        },
                        "Proj": {  # Project
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "ttl": {"type": "string"},           # title
                                    "desc": {"type": "string"},          # description
                                    "tech": {"type": "string"},          # technologies_used
                                    "role": {"type": "string"},          # role
                                },
                                "required": ["id", "ttl"]
                            },
                        },
                        "Skill": {  # Skill
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "name": {"type": "string"}
                                },
                                "required": ["id", "name"]
                            },
                        },
                        "Cert": {  # Certification
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "name": {"type": "string"},
                                    "issuer": {"type": "string"},        # issuing_organization
                                    "exp": {"type": "string"},           # expiration_date
                                },
                                "required": ["id", "name"]
                            },
                        },
                        "SSkill": {  # SoftSkill
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "name": {"type": "string"}
                                },
                                "required": ["id", "name"]
                            },
                        },
                        "JD": {  # JobDescription
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},                # Unique identifier
                                "comp": {"type": "string"},              # company
                                "req": {"type": "string"},               # requirements
                                "resp": {"type": "string"},              # responsibilities
                                "loc": {"type": "string"},               # location
                            },
                            "required": ["id", "comp"]
                        },
                        "JTitle": {  # JobTitle
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},                # Unique identifier
                                "ttl": {"type": "string"},               # title
                                "lvl": {"type": "string"},               # level
                                "cat": {"type": "string"},               # category
                            },
                            "required": ["id"]  # 'ttl' is optional
                        },
                        "JKeyword": {  # JobKeyword
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "keyword": {"type": "string"}
                                },
                                "required": ["id", "keyword"]
                            },
                        },
                        "Indus": {  # Industry
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},            # Unique identifier
                                    "name": {"type": "string"}
                                },
                                "required": ["id", "name"]
                            },
                        },
                    },
                },
                "rels": {  # relationships
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "s_type": {"type": "string"},              # start_node_type
                            "s_id": {"type": "string"},                # start_node_id
                            "rel": {"type": "string"},                 # relationship_type
                            "e_type": {"type": "string"},              # end_node_type
                            "e_id": {"type": "string"},                # end_node_id
                        },
                        "required": ["s_type", "s_id", "rel", "e_type", "e_id"]
                    },
                },
            },
            "required": ["nodes", "rels"],
        },
    }
]



# Mapping from LLM 'id's to node attribute keys, per batch
llm_id_to_attr_key = {}

# Helper functions
def get_or_create_node_id(node_type, node_value):
    global node_id_counter
    node_dict = node_mappings[node_type]
    if isinstance(node_value, dict):
        # Filter out empty or null values, excluding 'id'
        filtered_items = {k: v for k, v in node_value.items() if v and k != 'id'}
        key = tuple(sorted(filtered_items.items()))
    else:
        key = node_value.lower()

    if key in node_dict:
        return node_dict[key], False, key
    else:
        node_id = node_id_counter
        node_id_counter += 1
        node_dict[key] = node_id
        return node_id, True, key

def process_singular_entity(node_type, node_writer, keys, node_values):
    llm_id = node_values.get('id')
    if not llm_id:
        print(f"No 'id' found for {node_type} node.")
        return None

    meaningful_data = any(v for k, v in node_values.items() if v and k != 'id')
    if not meaningful_data:
        print(f"Skipping empty {node_type} node.")
        return None

    node_id, is_new, attr_key = get_or_create_node_id(node_type, node_values)
    llm_id_to_attr_key[llm_id] = (node_type, attr_key)

    if is_new:
        row_data = {'id': node_id}
        row_data.update({key: node_values.get(key, '') for key in keys if key != 'id'})
        node_writer.writerow(row_data)
        node_files[node_type].flush()
    return node_id


def process_list_of_entities(node_type, node_writer, keys, node_values_list):
    ids = []
    for node in node_values_list:
        llm_id = node.get('id')
        if not llm_id:
            print(f"No 'id' found for {node_type} node.")
            continue

        node_id, is_new, attr_key = get_or_create_node_id(node_type, node)
        llm_id_to_attr_key[llm_id] = (node_type, attr_key)

        if is_new:
            row_data = {'id': node_id}
            row_data.update({key: node.get(key, '') for key in keys if key != 'id'})
            node_writer.writerow(row_data)
            node_files[node_type].flush()
        ids.append(node_id)
    return ids

def get_node_id_from_llm_id(llm_id):
    mapping = llm_id_to_attr_key.get(llm_id)
    if not mapping:
        return None
    node_type, attr_key = mapping
    return node_mappings[node_type].get(attr_key)

def process_singular_string_entity(node_type, node_writer, keys, node_value):
    node_id, is_new = get_or_create_node_id(node_type, node_value)
    print(f"Processing singular string entity for {node_type}, is_new={is_new}")
    if is_new:
        key_name = 'name' if 'name' in keys else 'keyword'
        row_data = {'id': node_id, key_name: node_value}
        node_writer.writerow(row_data)
        node_files[node_type].flush()
        print(f"Wrote new {node_type} node to CSV: {row_data}")
    else:
        print(f"{node_type} node already exists: {node_value}")
    return node_id

# Function to retrieve node ID based on type and reference
def get_node_id(node_type, node_ref, node_ids):
    if isinstance(node_ref, int):
        # Index-based reference
        node_list = node_ids.get((node_type, 'list'), [])
        if node_ref < len(node_list):
            return node_list[node_ref]
        else:
            print(f"Invalid node index {node_ref} for node type {node_type}")
            return None
    else:
        # Name-based reference (case-insensitive)
        key = node_ref.lower()
        return node_mappings[node_type].get(key)


# Process each row in the dataset
for index, row in data.iterrows():
    #if index == 3146:
    #   break

    # Skip rows where 'label' is 'No Fit'
    if row['label'].strip().lower() == 'no fit':
        print(f"Skipping index {index} due to label 'No Fit'.")
        continue

    resume_text = row['resume_text']
    job_description_text = row['job_description_text']
    label = row['label']
    candidate_id = f"candidate_{index}"  # Generate a unique candidate_id
    job_id = f"job_{index}"  # Generate a unique job_id

    # Generate the prompt
    prompt = generate_prompt(resume_text, job_description_text)

    # Initialize retry counter
    retry_count = 0
    success = False

    MAX_RETRIES = 3

    while retry_count < MAX_RETRIES and not success:
        try:
            # Call the OpenAI API with function calling
            response = client.chat.completions.create(
                model='gpt-4o-mini',  # Updated model version
                messages=[
                    {"role": "system", "content": "You are an expert data annotator."},
                    {"role": "user", "content": prompt}
                ],
                functions=function_schema,
                function_call={"name": "extract_entities_and_relationships"},
                max_tokens=2000,  # Adjusted to prevent truncation
                temperature=0,
                top_p=1,
                n=1,
                stop=None,
            )

            # Extract the function call response using attribute access
            message = response.choices[0].message

            if message.function_call:
                function_args = message.function_call.arguments
                print(f"Function Arguments at index {index}: {function_args}")
                try:
                    extracted_data = json.loads(function_args)
                    success = True
                except json.JSONDecodeError as e:
                    print(f"Failed to parse function arguments at index {index}. Error: {e}")
                    print(f"Function Arguments: {function_args[:500]}...")  # Print first 500 chars for inspection
                    extracted_data = None
            else:
                print(f"No function call in response at index {index}.")
                extracted_data = None

        except openai.BadRequestError as e:
            print(f"OpenAI API request failed at index {index}: {e}")
            break  # Skip to the next row
        except openai.OpenAIError as e:
            print(f"OpenAI API encountered an error at index {index}: {e}")
            retry_count += 1
            print(f"Retrying... ({retry_count}/{MAX_RETRIES})")
            time.sleep(2)  # Wait before retrying

    if not success:
        print(f"Skipping index {index} after {MAX_RETRIES} failed attempts.")
        continue

    if extracted_data:
        print(f"Parsed data at index {index}: {extracted_data}")
        # Process nodes
        node_ids = {}  # To store the IDs of nodes extracted in this iteration
        extracted_nodes = extracted_data.get('nodes', {})
        relationships_list = extracted_data.get('rels', [])

        # Process each node type
        for node_type, node_values in extracted_nodes.items():
            if node_type in node_types:
                node_writer = node_writers[node_type]
                keys = node_types[node_type]

                if isinstance(node_values, dict):
                    print(f"Processing singular entity for {node_type}")
                    node_id = process_singular_entity(node_type, node_writer, keys, node_values)
                    node_ids[(node_type, 'single')] = node_id
                elif isinstance(node_values, list):
                    print(f"Processing list entities for {node_type}")
                    ids = process_list_of_entities(node_type, node_writer, keys, node_values)
                    node_ids[(node_type, 'list')] = ids
                elif isinstance(node_values, str):
                    print(f"Processing singular string entity for {node_type}")
                    node_id = process_singular_string_entity(node_type, node_writer, keys, node_values)
                    node_ids[(node_type, 'single')] = node_id
                else:
                    print(f"Unexpected data type for node_type {node_type} at index {index}")
            else:
                print(f"Unknown node type: {node_type} at index {index}")

        # Process relationships
        for rel in relationships_list:
            s_type = rel.get('s_type')  # start_node_type
            e_type = rel.get('e_type')  # end_node_type
            s_id = rel.get('s_id')  # start_node_id from LLM
            e_id = rel.get('e_id')  # end_node_id from LLM

            rel_type = rel.get('rel')    # relationship_type

            start_node_id = get_node_id_from_llm_id(s_id)
            if not start_node_id:
                print(f"Start node with LLM id '{s_id}' not found for relationship at index {index}")
                continue

            end_node_id = get_node_id_from_llm_id(e_id)
            if not end_node_id:
                print(f"End node with LLM id '{e_id}' not found for relationship at index {index}")
                continue

            # Write relationship
            relationships_writer.writerow({
                'start_node_id': start_node_id,
                'relationship_type': rel_type,
                'end_node_id': end_node_id
            })
            relationships_file.flush()
            print(f"Wrote relationship: {rel_type} from {s_type}({start_node_id}) to {e_type}({end_node_id})")
        # After processing relationships
        llm_id_to_attr_key.clear()
    else:
        print(f"Skipping index {index} due to parsing error.")

# Close all node CSV files
for node_file in node_files.values():
    node_file.close()

# Close relationships CSV file
relationships_file.close()

print("Data extraction complete. CSV files are saved in the 'neo4j_csv' directory.")
