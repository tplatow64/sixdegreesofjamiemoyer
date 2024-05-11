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
with driver.session(database="neo4j") as session:
    print('session defined')

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


    @app.route("/")
    def index():
        value = find_person('rojasjo03')
        return f"Hello World! {value}"
