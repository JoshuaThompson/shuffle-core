import os
import psycopg2
import psycopg2.extras
import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

conn = None

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get-matching-streams", methods=['POST', 'GET'])
def get_matching_streams():
    global conn
    if conn is None:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname=os.environ.get("POSTGRES_DB", ""),
            user=os.environ.get("POSTGRES_USER", ""),
            password=os.environ.get("POSTGRES_PASSWORD", "")
        )

    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    no_high_viewer_streams = request.form['no_high_viewer_streams']

    if no_high_viewer_streams == 'true':
        cur.execute("""
            SELECT c.name, c.logo, c.status, c.game, c.views, s.viewers
            FROM streams s
            INNER JOIN channels c ON s.channel_id = c.channel_id
            WHERE c.language = %s AND s.viewers >= 5 AND s.viewers <= 350
        """, (request.form['language'],))
    else:
        cur.execute("""
            SELECT c.name, c.logo, c.status, c.game, c.views, s.viewers
            FROM streams s
            INNER JOIN channels c ON s.channel_id = c.channel_id
            WHERE c.language = %s AND s.viewers >= 5
        """, (request.form['language'],))
    
    results = cur.fetchall()

    cur.close()

    return jsonify(**random.choice(results))