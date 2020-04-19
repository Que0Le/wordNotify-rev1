# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import request, jsonify
from flask import render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import json
import requests
import os, time
import threading, queue
import re
import itertools
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

MAX_DB_RANGE = 50000
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

def getDictTableName(db, dict_id):
    r = db.execute(f"select table_name from ALL_DICTS where id={dict_id}").fetchone()
    if r:
        return r["table_name"]
    return None

def respError(mess):
    return jsonify({"response": mess, "status": "error"})
def respSucc(mess):
    return jsonify({"response": mess, "status": "success"})

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

test_settings = False
temp_json = '''
{
    "notification": {
        "dict_dbs_to_notify": [
            "EN_DE",
            "DE_EN",
            "FR_EN"
        ]
    }
}'''
@bp.route('/api/v1/settings', methods=['GET', 'POST'])
@auth.login_required
def app_settings():
    if request.method == 'GET':
        global_config = current_app.config["GLOBAL_CONFIG"]
        if test_settings:
            return json.loads(temp_json)
        return global_config
    elif request.method == 'POST':
        new_config = request.json
        error = current_app.config["GLOBAL_SF"].verify_config(new_config)
        if error == "":
            current_app.config["GLOBAL_SF"].writeConfigToJsonFile(new_config)
            handyfunctions.update_config(current_app, new_config)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": error})

@bp.route("/settings")
@auth.login_required
def settings_page():
    return render_template("settings.html")

@bp.route("/dicts/<int:dict_id>/words/word_id")
@auth.login_required
def view_word_page():
    dict_dbname = getDictTableName(db, dict_id)
    if not dict_dbname:
        return page_not_found(404)
    return render_template("view_word.html")

@bp.route('/api/v1/dicts/<int:dict_id>/words', 
                    methods=['GET', 'POST', 'PUT'])
def words_handler(dict_id):
    db = get_db()
    dict_dbname = getDictTableName(db, dict_id)
    if not dict_dbname:
        return respSucc("dict id not found in database")
    ############# GET
    if request.method == 'GET':
        try:
            print(f"getting all words for dict_id {dict_id}")
            r = db.execute(f"select max(rowid) from {dict_dbname};\
                ").fetchone()
            if int(r["max(rowid)"]) > MAX_DB_RANGE:
                return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /words/1-{MAX_DB_RANGE}")
            r = db.execute(f"select * from {dict_dbname} where true;\
                ").fetchall()
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"error getting words for dict_id {dict_id}")
    ############# POST
    elif request.method == 'POST':
        r = request.json
        # TODO: verify r (word-class?)
        try:
            c = db.cursor()
            c.execute(f"insert into {dict_dbname}( \
                id, line, note, description, date_created, last_modified \
                ) values (?,?,?,?,?,?)", (
                    None, r["line"], r["note"], r["description"], 
                    r["date_created"], r["last_modified"])
                )
            db.commit()
            r["id"] = c.lastrowid
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError("Error write word to database")
    ############# PUT
    elif request.method == 'PUT':
        r = request.json
        # TODO: verify r (word-class?)
        word_id = r["id"]
        try:
            db.execute(f"""update {dict_dbname} \
                set line=?, note=?, description=?, date_created=?, last_modified=? \
                where id=?
                """, (
                    r["line"], r["note"], r["description"], 
                    r["date_created"], r["last_modified"], word_id)
            )
            db.commit()
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"Error edit word with id {word_id} in database")

    return respError("unknow error")


@bp.route('/api/v1/dicts/<int:dict_id>/words/<word_id_raw>', 
                    methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def words_id_handler(dict_id, word_id_raw):
    db = get_db()
    dict_dbname = getDictTableName(db, dict_id)
    if not dict_dbname:
        return respSucc("dict id not found in database")
    # get word id from url
    word_id = None
    rand = None
    top, bot = None, None
    if word_id_raw=="":
        # Get all words in DB. 
        pass
    elif word_id_raw.isnumeric():
        word_id=int(word_id_raw)
    elif word_id_raw == "random":
        rand = True
    else:
        temp = re.findall(r"([0-9]+)-([0-9]+)", word_id_raw)
        if len(temp) == 0:
            return respError("word id must be numberic or range 123-456")
        (bot, top) = temp[0]
        if abs(int(top)-int(bot)) > MAX_DB_RANGE:
            return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /words/1-{MAX_DB_RANGE}")
    ############# GET
    if request.method == 'GET':
        try:
            if word_id:
                r = db.execute(f"select * from {dict_dbname} where \
                    id={word_id};").fetchone()
            else:
                if rand:
                    r = db.execute(f"select * from {dict_dbname} where \
                        rowid=(abs(random()) % (select (select max(rowid) from {dict_dbname}))+1);\
                        ").fetchone()
                elif top and bot:
                    r = db.execute(f"SELECT * FROM {dict_dbname} WHERE \
                        id between {bot} and {top};\
                        ").fetchall()
            if r:
                return respSucc(r)
            else:
                return respError(f"word with id {word_id_raw} not found")
        except:
            print(traceback.format_exc())
            return respError(f"error getting {word_id_raw}")
    ############# DEL
    elif request.method == 'DELETE':
        if not word_id:
            return respError("word id not supplied")
        try:
            db.execute(f"delete from {dict_dbname} where \
                id={word_id}")
            db.commit()
            return respSucc(word_id)
        except:
            print(traceback.format_exc())
            return respError(f"error deleting word id {word_id}")

    return respError("unknow error")

@bp.route('/api/v1/dicts/', methods=['GET', 'POST', 'PUT'])
@auth.login_required
def dicts_handler():
    db = get_db()
    dict_dbname = "ALL_DICTS"
    ############# GET
    if request.method == 'GET':
        try:
            r = db.execute(f"select max(rowid) from {dict_dbname};\
                ").fetchone()
            if int(r["max(rowid)"]) > MAX_DB_RANGE:
                return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /dicts/1-{MAX_DB_RANGE}")
            r = db.execute(f"select * from {dict_dbname} where true;\
                ").fetchall()
            return respSucc(r)
        except: 
            print(traceback.format_exc())
            return respError(f"error getting dicts")
    ############# POST
    elif request.method == 'POST':
        r = request.json
        try:
            c = db.cursor()
            c.execute(f"insert into {dict_dbname}( \
                id, table_name, size \
                ) values (?,?,?)", (None, r["table_name"], r["size"])
            )
            db.commit()
            r["id"] = c.lastrowid
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError("Error POST dict to database")
    ############# PUT
    elif request.method == 'PUT':
        r = request.json
        dict_id = r["id"]
        try:
            db.execute(f"""update {dict_dbname} \
                set table_name=?, size=?\
                where id=?
                """, (r["table_name"], r["size"], dict_id)
            )
            db.commit()
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"Error edit dict with id {dict_id} in database")

    return respError("unknow error")


@bp.route('/api/v1/dicts/<dict_id_raw>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def dicts_id_handler(dict_id_raw):
    db = get_db()
    dict_dbname = "ALL_DICTS"
    ############# TEST
    dict_id = None
    rand = None
    top, bot = None, None
    if dict_id_raw=="":
        # Get all words in DB. 
        # TODO: But too large DB will break sending back
        pass
    elif dict_id_raw.isnumeric():
        dict_id=int(dict_id_raw)
    elif dict_id_raw == "random":
        rand = True
    else:
        temp = re.findall(r"([0-9]+)-([0-9]+)", dict_id_raw)
        if len(temp) == 0:
            return respError("dict_id must be numberic or range 123-456")
        (bot, top) = temp[0]
        if abs(int(top)-int(bot)) > MAX_DB_RANGE:
            return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /words/1-{MAX_DB_RANGE}")
    ############# GET
    if request.method == 'GET':
        try:
            if dict_id:
                r = db.execute(f"select * from {dict_dbname} where \
                    id={dict_id};").fetchone()
            else:
                if rand:
                    r = db.execute(f"select * from {dict_dbname} where \
                        rowid=(abs(random()) % (select (select max(rowid) from {dict_dbname}))+1);\
                        ").fetchone()
                elif top and bot:
                    r = db.execute(f"SELECT * FROM {dict_dbname} WHERE \
                        id between {bot} and {top};\
                        ").fetchall()
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"error getting {dict_id_raw}")
    ############# DEL
    elif request.method == 'DELETE':
        if not dict_id:
            return respError("dict id not supplied")
        try:
            db.execute(f"delete from {dict_dbname} where \
                id={dict_id}")
            db.commit()
            return respSucc(dict_id)
        except:
            print(traceback.format_exc())
            return respError(f"error deleting dict id {dict_id}")

    return respError("unknow error")