from flask import Flask, redirect, url_for, request, render_template
from neo4j import GraphDatabase
from py2neo import Graph
import json
import os
import requests

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
uri = app.config.get('NEO_URI')
pwd = app.config.get('NEO_PWD')
print('connecting')
driver = GraphDatabase.driver(uri, auth=("neo4j", pwd))
print('connected')

def find_person(id: str) -> json:
    print(f'finding {id}')
    try:
        neo4j_session = driver.session(database="neo4j")
        print('session defined')
        query = f"""MATCH (p:Person)
            WHERE p.debut <> "" AND p.playerID = $p1
            RETURN p.playerID as playerID, p.name + ' ' + left(p.debut,4) + ' - ' + left(p.finalGame, 4) AS name
            ORDER BY p.nameLast      
            """
        ret_val = neo4j_session.run(query, p1=id)
        print(f'query done {ret_val.data()[0]['name']}')
        neo4j_session.close()
    except Exception as e:
        print(f"error querying database {e}")
    return ret_val.data()[0]['name']


@app.route("/")
def index():
    print('in function')
    value = find_person('rojasjo03')
    return f"Hello World! {value}"
