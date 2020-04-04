# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import request, jsonify
from flask import render_template, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import time
import threading
import json
import requests
from handyfunctions import *
from localapp import *


game = myGame()
############################
app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

users = {
    "tom": generate_password_hash("thisIStom"),
    "jerry": generate_password_hash("ThatisJerry")
}
auth = HTTPBasicAuth()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getTablesInfo():
    conn = sqlite3.connect('testdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()     
    all_dicts = cur.execute("SELECT * FROM ALL_DICTS;").fetchall()
    return all_dicts

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/', methods=['GET'])
def home():
    return render_template('dict_corona.html', mess="test site work")


# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     conn = sqlite3.connect('books.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()     
#     all_books = cur.execute('SELECT * FROM books;').fetchall()

#     return jsonify(all_books)

@app.route('/api/v1/resources/available_dicts', methods=['GET'])
@auth.login_required
def available_dicts():
    conn = sqlite3.connect('testdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()     
    # all_dicts = cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';").fetchall()
    all_dicts = cur.execute("SELECT * FROM ALL_DICTS;").fetchall()
    # print(all_dicts)
    # flat_list = [item for sublist in all_dicts for item in sublist]
    return jsonify(all_dicts)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/dicts', methods=['GET'])
@auth.login_required
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    rand = query_parameters.get('random')
    lang_temp = query_parameters.get('lang')
    lang = ""
    i=-1
    all_dicts = getTablesInfo()
    for index, d in enumerate(all_dicts):
        if d["table_name"] == lang_temp:
            lang = lang_temp
            i=index
    if not (lang!= "" and (rand or id)):
        return page_not_found(404)
    
    query = f"SELECT * FROM {lang} WHERE"
    to_filter = []

    if rand=="true":
        rand_id = random.randint(1, all_dicts[i]["size"])
        query += ' id=? AND'
        to_filter.append(str(rand_id))
    if id:
        query += ' id=? AND'
        to_filter.append(id)

    query = query[:-4] + ';'

    conn = sqlite3.connect('testdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


if __name__ == "__main__":
    game.start()
    app.run(port=5000, host='0.0.0.0', debug=True, use_reloader=True)


# while True:
#     print("tada")
#     time.sleep(1)
    




