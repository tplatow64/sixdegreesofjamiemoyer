from flask import Flask
import os
from neo4j import GraphDatabase
from py2neo import Graph
import json

app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
uri = app.config.get('NEO_URI')
pwd = app.config.get('NEO_PWD')

driver = GraphDatabase.driver(uri, auth=("neo4j", pwd))

def find_person(id: str) -> json:
    print(f'finding {id}')
    query = f"""MATCH (p:Person)
        WHERE p.debut <> "" AND p.playerID = $p1
        RETURN p.playerID as playerID, p.name + ' ' + left(p.debut,4) + ' - ' + left(p.finalGame, 4) AS name
        ORDER BY p.nameLast      
        """
    ret_val = session.run(query, p1=id)
    print('query done')
    return ret_val.data()[0]['name']


# @app.route("/")
# def index():
#     return "Hello World!"
with driver.session(database="neo4j") as session:
    @app.route("/")
    def index():
        # return f"URI is {uri}"
        print('find person')
        return find_person('rojasjo03')
        # return ('hi')

    app.run(host='0.0.0.0', port=17758, debug=True)
    #app.run()

