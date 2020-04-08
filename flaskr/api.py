# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import request, jsonify
from flask import render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import threading
import json
import requests
import os, time
import threading, queue
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flaskr import handyfunctions

from flaskr.auth import login_required
from flaskr.db import get_db
from flask import current_app
import traceback
bp = Blueprint("api", __name__)


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
    users = current_app.config['USERS']
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@bp.route('/', methods=['GET'])
def home():
    return render_template('dict_corona.html', mess="test site work")

@bp.route('/api/v1/resources/available_dicts', methods=['GET'])
def available_dicts():
    db = get_db()
    try:
        all_dicts = db.execute(
        "SELECT * FROM ALL_DICTS;"
        ).fetchall()
        print(all_dicts)
        return jsonify(all_dicts)
    except Exception:
        print(traceback.format_exc())
        return page_not_found(404)
    

@bp.route('/api/v1/resources/settings', methods=['GET', 'POST'])
@auth.login_required
def app_settings():
    if request.method == 'GET':
        global_config = current_app.config["GLOBAL_CONFIG"]
        return global_config
    elif request.method == 'POST':
        new_config = request.json
        error = current_app.config["GLOBAL_SF"].verify_config(new_config)
        if error == "":
            current_app.config["GLOBAL_SF"].writeConfigToJsonFile(new_config)
            handyfunctions.update_config(new_config, current_app)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": error})


@bp.route('/api/v1/resources/dicts', methods=['GET'])
@auth.login_required
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    rand = query_parameters.get('random')
    dict_db = query_parameters.get('dict_db')

    if not (dict_db!= "" and (rand or id)):
        return page_not_found(404)
    
    query = f"SELECT * FROM {dict_db} WHERE"

    if rand=="true":
        # select * from DE_EN where rowid = (abs(random()) % (select (select max(rowid) from DE_EN)+1));
        query += f' rowid=(abs(random()) % (select (select max(rowid) from {dict_db})+1)) AND'
    if id:
        query += f' id={id} AND'

    query = query[:-4] + ';'

    db = get_db()
    try:
        result = db.execute(query).fetchall()
        return jsonify(result)
    except Exception:
        print(traceback.format_exc())
        return page_not_found(404)

# @bp.route('/api/v1/resources/dict_db/<dict_db_name>', methods=['GET', 'POST'])
# @auth.login_required
# def dict_db_handler(dict_db_name):
#     if request.method == 'GET':
#         config = sf.readConfigFile()
#         print(config)
#         return config
#     elif request.method == 'POST':