from neo4j import GraphDatabase

uri = "neo4j+ssc://7bf5a48e.databases.neo4j.io"  # Update with your Neo4j URI
username = "neo4j"             # Update with your username
password = "oxsK7V5_86emZlYQlvCfQHfVWS95wXz29OhtU8GAdFc"          # Update with your password

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("SHOW INDEXES")
    for record in result:
        print(record["name"])
