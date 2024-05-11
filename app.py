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


@app.route("/")
def index():
    return f"Hello World! {uri}"
