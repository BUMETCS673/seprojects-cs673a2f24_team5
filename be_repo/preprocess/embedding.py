# embedding_generation.py
import pandas as pd
import json
import os
import time
from tqdm import tqdm
import logging


# Initialize the OpenAI API client
from configs.openai_client import get_openai_client

client = get_openai_client()

# Setup logging
log_file = 'embedding_generation.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Initialize the embedding model
default_model = "text-embedding-ada-002"  # Updated to a commonly used model

# Directory containing the original CSV files
csv_dir = 'neo4j_csv'

# Directory to save updated CSV files with embeddings
updated_csv_dir = 'neo4j_csv_with_embeddings'
os.makedirs(updated_csv_dir, exist_ok=True)

# Node types and their attributes
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

# Load node CSV files into DataFrames
node_dfs = {}
for node_type in node_types.keys():
    file_path = os.path.join(csv_dir, f'{node_type}.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        node_dfs[node_type] = df
    else:
        print(f"CSV file for node type '{node_type}' not found in '{csv_dir}'.")

# Function to generate embeddings for a node DataFrame
def generate_embeddings_for_node(df, attributes, model, client, batch_size=100):
    # Exclude 'id' from attributes to be concatenated
    text_attributes = [attr for attr in attributes if attr not in ['id', 'embedding']]
    # Concatenate all text attributes into a single string per row
    texts = df[text_attributes].fillna('').astype(str).agg(' '.join, axis=1).tolist()
    
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings in batches"):
        batch_texts = texts[i:i+batch_size]
        if i == 1:
            break
        try:
            response = client.embeddings.create(input=batch_texts, model=model)

            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
            time.sleep(1)  # To respect rate limits; adjust as necessary
        except Exception as e:
            print(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
            # Optionally, append None or a placeholder
            embeddings.extend([None] * len(batch_texts))
    
    if len(embeddings) != len(texts):
        raise ValueError("Number of embeddings does not match number of texts.")
    
    return embeddings

# Generate embeddings for each node type
for node_type, df in node_dfs.items():
    print(f"Generating embeddings for node type '{node_type}'...")
    attributes = node_types[node_type]
    # Generate embeddings
    embeddings = generate_embeddings_for_node(df, attributes, default_model, client)
    # Add embeddings to the DataFrame
    df['embedding'] = embeddings
    # Update the DataFrame in the dictionary
    node_dfs[node_type] = df

# Save updated node CSV files with embeddings
for node_type, df in node_dfs.items():
    # Convert embedding arrays to JSON strings for storage
    if 'embedding' in df.columns:
        df['embedding'] = df['embedding'].apply(lambda x: json.dumps(x) if isinstance(x, list) else '[]')
    # Save the updated DataFrame to a CSV file
    file_path = os.path.join(updated_csv_dir, f'{node_type}.csv')
    df.to_csv(file_path, index=False)
    print(f"Updated CSV file saved for node type '{node_type}'.")

print("Embedding generation and CSV update completed.")
