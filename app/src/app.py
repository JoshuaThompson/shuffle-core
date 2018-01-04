import os
from flask import Flask, render_template, request

app = Flask(__name__)

host = "db"
port = "5432"
dbname = os.environ.get("POSTGRES_DB", "")
user = os.environ.get("POSTGRES_USER", "")
password = os.environ.get("POSTGRES_PASSWORD", "")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get-matching-streams", methods=['POST'])
def get_matching_streams():
    #get matching streams
    return "Hello World!"