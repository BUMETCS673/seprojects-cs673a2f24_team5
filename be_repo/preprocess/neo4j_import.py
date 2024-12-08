# neo4j_import.py

import pandas as pd
from neo4j import GraphDatabase
import json
import os
from tqdm import tqdm
import logging
from configs.database import get_key_database

keys_db = get_key_database()
keys_collection = keys_db["keys"]

# Neo4j Connection Details
NEO4J_URI = keys_collection.find_one({"_id": "NEO4J_URI"})["api_key"]  # Replace with your Neo4j URI
NEO4J_USERNAME = "neo4j"  # Replace with your Neo4j username
NEO4J_PASSWORD = keys_collection.find_one({"_id": "NEO4J_PASSWORD"})["api_key"]  # Replace with your Neo4j password

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory containing the updated CSV files with embeddings
csv_dir = 'neo4j_csv_with_embeddings'

# Node types and their attributes
node_types = {
    'Edu': ['id', 'deg', 'f_study', 'inst', 's_year', 'e_year', 'gpa', 'embedding'],
    'WE': ['id', 'pos', 'comp', 'loc', 'embedding'],
    'Proj': ['id', 'ttl', 'desc', 'tech', 'role', 'embedding'],
    'Skill': ['id', 'name', 'embedding'],
    'Cert': ['id', 'name', 'issuer', 'exp', 'embedding'],
    'SSkill': ['id', 'name', 'embedding'],
    'JD': ['id', 'comp', 'req', 'resp', 'loc', 'embedding'],
    'JTitle': ['id', 'ttl', 'lvl', 'cat', 'embedding'],
    'JKeyword': ['id', 'keyword', 'embedding'],
    'Indus': ['id', 'name', 'embedding'],
}

# Neo4j connection details from environment variables
uri = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

# Initialize Neo4j driver
driver = GraphDatabase.driver(uri, auth=AUTH)

# Verify connectivity
try:
    driver.verify_connectivity()
    logger.info("Successfully connected to Neo4j.")
except Exception as e:
    logger.error(f"Failed to connect to Neo4j: {e}")
    driver.close()
    exit(1)


# Function to load node CSV files into DataFrames
def load_node_dataframes(csv_dir, node_types):
    node_dfs = {}
    for node_type in node_types.keys():
        file_path = os.path.join(csv_dir, f'{node_type}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            node_dfs[node_type] = df
            logger.info(f"Loaded {len(df)} records for node type '{node_type}'.")
        else:
            logger.warning(f"CSV file for node type '{node_type}' not found in '{csv_dir}'.")
    return node_dfs


# Function to load relationships CSV file into a DataFrame
def load_relationships_data(csv_dir):
    relationships_file = os.path.join(csv_dir, 'relationships.csv')
    if os.path.exists(relationships_file):
        df = pd.read_csv(relationships_file)
        logger.info(f"Loaded {len(df)} relationship records.")
        return df
    else:
        logger.warning(f"Relationships CSV file not found in '{csv_dir}'.")
        return None


# Function to create constraints
def create_constraints(driver):
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Edu) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:WE) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Proj) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Skill) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Cert) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:SSkill) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:JD) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:JTitle) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:JKeyword) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Indus) REQUIRE n.id IS UNIQUE",
    ]
    with driver.session() as session:
        for constraint in constraints:
            try:
                session.run(constraint)
                logger.info(f"Executed constraint: {constraint}")
            except Exception as e:
                logger.error(f"Failed to execute constraint '{constraint}': {e}")
    logger.info("Constraints created or already exist.")


def standardize_relationship_types(df):
    if 'relationship_type' in df.columns:
        original_types = df['relationship_type'].unique()
        df['relationship_type'] = df['relationship_type'].str.upper().str.replace(' ', '_').str.replace('[^A-Z0-9_]',
                                                                                                        '', regex=True)
        standardized_types = df['relationship_type'].unique()
        logger.info(
            f"Standardized relationship types from {len(original_types)} to {len(standardized_types)} unique types.")
    return df


# Function to import nodes into Neo4j in batches
def import_nodes_in_batches(tx, node_type, df, batch_size=1000):
    columns = df.columns.tolist()
    # Prepare property assignments excluding 'id'
    set_props = ', '.join([f"n.{col} = row.{col}" for col in columns if col != 'id'])
    query = f"""
    UNWIND $rows AS row
    MERGE (n:{node_type} {{ id: toInteger(row.id) }})
    ON CREATE SET
        {set_props}
    """
    # Convert embedding JSON strings back to lists if present
    if 'embedding' in df.columns:
        df['embedding'] = df['embedding'].apply(lambda x: json.loads(x) if pd.notnull(x) else [])
    data = df.to_dict('records')
    for i in tqdm(range(0, len(data), batch_size), desc=f"Importing {node_type} in batches"):
        batch = data[i:i + batch_size]
        try:
            tx.run(query, rows=batch)
            logger.info(f"Imported batch {i // batch_size + 1} for node type '{node_type}'.")
        except Exception as e:
            logger.error(f"Error importing batch {i // batch_size + 1} for node type '{node_type}': {e}")


# Function to create a mapping from ID to node type
def create_id_to_type_mapping(node_dfs):
    id_to_type = {}
    for node_type, df in node_dfs.items():
        for node_id in df['id']:
            try:
                id_to_type[int(node_id)] = node_type
            except ValueError:
                logger.warning(f"Invalid ID '{node_id}' in node type '{node_type}'. Skipping.")
    logger.info("Created ID to node type mapping.")
    return id_to_type


# Function to infer node types for relationships
def infer_node_types(rel_df, id_to_type):
    rel_df['start_node_type'] = rel_df['start_node_id'].apply(lambda x: id_to_type.get(int(x), 'Unknown'))
    rel_df['end_node_type'] = rel_df['end_node_id'].apply(lambda x: id_to_type.get(int(x), 'Unknown'))
    unknown_start = rel_df[rel_df['start_node_type'] == 'Unknown']
    unknown_end = rel_df[rel_df['end_node_type'] == 'Unknown']
    if not unknown_start.empty or not unknown_end.empty:
        logger.warning("Some node IDs could not be mapped to any node type.")
        logger.warning("Unknown Start Nodes:")
        logger.warning(unknown_start)
        logger.warning("Unknown End Nodes:")
        logger.warning(unknown_end)
    return rel_df


def import_relationships_in_batches(tx, df, batch_size=1000):
    data = df.to_dict('records')
    for i in tqdm(range(0, len(data), batch_size), desc="Importing relationships in batches"):
        batch = data[i:i + batch_size]
        unwind_data = [
            {
                "start_id": int(rel['start_node_id']),
                "end_id": int(rel['end_node_id']),
                "rel_type": rel['relationship_type']
            }
            for rel in batch
        ]
        query = """
        UNWIND $rows AS row
        MATCH (a {id: row.start_id})
        MATCH (b {id: row.end_id})
        CALL apoc.merge.relationship(a, row.rel_type, {}, {}, b) YIELD rel
        RETURN rel
        """
        try:
            tx.run(query, rows=unwind_data)
            logger.info(f"Imported batch {i // batch_size + 1} of relationships.")
        except Exception as e:
            logger.error(f"Error importing batch {i // batch_size + 1} of relationships: {e}")


# Main function to perform the import
def main():
    # Load node and relationship data
    node_dfs = load_node_dataframes(csv_dir, node_types)
    relationship_df = load_relationships_data(csv_dir)

    # Create constraints
    create_constraints(driver)

    # Create ID to type mapping
    id_to_type = create_id_to_type_mapping(node_dfs)

    # Import nodes
    with driver.session() as session:
        for node_type, df in node_dfs.items():
            logger.info(f"Importing nodes for node type '{node_type}'...")
            session.execute_write(import_nodes_in_batches, node_type, df)
        logger.info("Node import completed.")

    # Import relationships
    if relationship_df is not None:
        # Standardize relationship types
        relationship_df = standardize_relationship_types(relationship_df)

        # Infer node types if not present
        if 'start_node_type' not in relationship_df.columns or 'end_node_type' not in relationship_df.columns:
            logger.info("Inferring 'start_node_type' and 'end_node_type' based on node IDs...")
            relationship_df = infer_node_types(relationship_df, id_to_type)

        # Check for unknown node types
        unknown_rels = relationship_df[
            (relationship_df['start_node_type'] == 'Unknown') |
            (relationship_df['end_node_type'] == 'Unknown')
            ]
        if not unknown_rels.empty:
            logger.error("Some relationships have unknown node types. Please verify your data.")
            logger.error(unknown_rels)
            # Skip unknown relationships
            relationship_df = relationship_df[
                (relationship_df['start_node_type'] != 'Unknown') &
                (relationship_df['end_node_type'] != 'Unknown')
                ]

        # Import relationships
        with driver.session() as session:
            logger.info("Importing relationships...")
            session.execute_write(import_relationships_in_batches, relationship_df)
            logger.info("Relationship import completed.")
    else:
        logger.info("No relationships to import.")

    driver.close()
    logger.info("Neo4j import completed.")


if __name__ == "__main__":
    main()
