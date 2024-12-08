from neo4j import GraphDatabase
from configs.database import get_key_database

keys_db = get_key_database()
keys_collection = keys_db["keys"]

# Neo4j Connection Details
NEO4J_URI = keys_collection.find_one({"_id": "NEO4J_URI"})["api_key"]  # Replace with your Neo4j URI
NEO4J_USERNAME = "neo4j"  # Replace with your Neo4j username
NEO4J_PASSWORD = keys_collection.find_one({"_id": "NEO4J_PASSWORD"})["api_key"]  # Replace with your Neo4j password

uri = NEO4J_URI  # Update with your Neo4j URI
username = NEO4J_USERNAME  # Update with your username
password = NEO4J_PASSWORD  # Update with your password

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("SHOW INDEXES")
    for record in result:
        print(record["name"])
