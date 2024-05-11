from flask import Flask
import os

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
uri = app.config.get('NEO_URI')

@app.route("/")
def index():
    return f"Hello World! {uri}"
