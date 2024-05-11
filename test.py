from neo4j import GraphDatabase

# Replace with the actual URI, username and password
AURA_CONNECTION_URI = "neo4j+ssc://165a3cce.databases.neo4j.io"
AURA_USERNAME = "neo4j"
AURA_PASSWORD = "t-wZUwiK3jKzw0NbPbN3SBuZwU-KPqcnJRDygBk-4bI"

# Driver instantiation
driver = GraphDatabase.driver(
    AURA_CONNECTION_URI,
    auth=(AURA_USERNAME, AURA_PASSWORD)
)

# Cypher query
gds_version_query = """MATCH (p:Person)
        RETURN p.playerID as playerID, p.name + ' ' + left(p.debut,4) + ' - ' + left(p.finalGame, 4) AS name
        ORDER BY p.nameLast      
        """

# Create a driver session
with driver.session() as session:
    # Use .data() to access the results array
    results = session.run(gds_version_query).data()
    print(results)

print("wow")