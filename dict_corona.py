# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import request, jsonify
from flask import render_template, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import threading
import json
import requests
from handyfunctions import *
from localClass import *
import os, time
import threading, queue

############################
app = flask.Flask(__name__)
# app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# users = {
#     "tom": generate_password_hash("thisIStom"),
#     "jerry": generate_password_hash("ThatisJerry")
# }
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
    all_dicts = cur.execute("SELECT * FROM ALL_DICTS;").fetchall()
    return jsonify(all_dicts)

@app.route('/api/v1/resources/settings', methods=['GET', 'POST'])
@auth.login_required
def app_settings():
    if request.method == 'GET':
        config = sf.readConfigFile()
        print(config)
        return config
    elif request.method == 'POST':
        global global_config
        global g_config_queue
        config = request.json
        error = sf.verify_config(config)
        if error == "":
            sf.writeConfigToJsonFile(config)
            global_config = config
            g_config_queue.put(global_config)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": error})

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/dicts', methods=['GET'])
@auth.login_required
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    rand = query_parameters.get('random')
    dict_db_temp = query_parameters.get('dict_db')
    dict_db = ""
    i=-1
    all_dicts = getTablesInfo()
    for index, d in enumerate(all_dicts):
        if d["table_name"] == dict_db_temp:
            dict_db = dict_db_temp
            i=index
    if not (dict_db!= "" and (rand or id)):
        return page_not_found(404)
    
    query = f"SELECT * FROM {dict_db} WHERE"

    if rand=="true":
        # select * from DE_EN where rowid = (abs(random()) % (select (select max(rowid) from DE_EN)+1));
        query += f' rowid=(abs(random()) % (select (select max(rowid) from {dict_db})+1)) AND'
    if id:
        query += f' id={id} AND'

    query = query[:-4] + ';'

    conn = sqlite3.connect('testdb.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query).fetchall()

    return jsonify(results)


if __name__ == "__main__":
    sf = SettingFile()
    global_config = sf.readConfigFile()

    # Auth API
    user = global_config["settings"]["API_username"]
    password = global_config["settings"]["API_password"]
    users = {
        user: generate_password_hash(password),
        "jerry": generate_password_hash("ThatisJerry")
    }
    encoded_u = base64.b64encode((user+":"+password).encode()).decode()

    # Prepare and run notifier in thread
    g_config_queue = queue.Queue()
    g_config_queue.put(global_config)
    notifierThead = NotifierThead(g_config_queue, encoded_u)
    notifierThead.start()

    app.run(port=5000, host='127.0.0.1', debug=True, use_reloader=True)


# while True:
#     print("tada")
#     time.sleep(1)
    




