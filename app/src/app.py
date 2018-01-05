import os
import psycopg2
import psycopg2.extras
import sys
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get-matching-streams", methods=['POST', 'GET'])
def get_matching_streams():
    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname=os.environ.get("POSTGRES_DB", ""),
        user=os.environ.get("POSTGRES_USER", ""),
        password=os.environ.get("POSTGRES_PASSWORD", "")
    )
    
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM streams s INNER JOIN channels c ON s.channel_id = c.channel_id LIMIT 10;")
    result = cur.fetchone()

    cur.close()

    return jsonify(**result)