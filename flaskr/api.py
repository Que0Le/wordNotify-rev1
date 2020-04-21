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
import os, time, datetime
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
from flaskr import custom_model

from flaskr.auth import login_required
from flaskr.db import get_db
from flask import current_app
import traceback
bp = Blueprint("api", __name__)

MAX_DB_RANGE = 50000    # max row return at once
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

@bp.route('/api/v1/settings', methods=['GET', 'POST'])
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
    m = custom_model.TB_VocabularyCollection(db, "")
    query_parameters = request.args
    columns = "*"
    if "columns" in query_parameters:
        columns_raw = query_parameters.get('columns')
        columns = ','.join(c for c in columns_raw.split("."))
    table_names = m.get_records_with_ids(
        table_name="ALL_DICTS", ids=[dict_id], columns="table_name")
    if len(table_names)==0:
        return respError(f"No dict with id {dict_id} found")
    dict_dbname = table_names[0]["table_name"]
    # print(dict_dbname)
    # dict_dbname = getDictTableName(db, dict_id)
    # if not dict_dbname:
    #     return respSucc("dict id not found in database")
    ############# GET###DONE
    if request.method == 'GET':
        try:
            print(f"getting all words for dict_id {dict_id}")
            # r = db.execute(f"select max(rowid) from {dict_dbname};\
            #     ").fetchone()
            s = m.get_size_of_table(table_name=dict_dbname)
            # if int(r["max(rowid)"]) > MAX_DB_RANGE:
            if int(s) > MAX_DB_RANGE:
                return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /words/1-{MAX_DB_RANGE}")
            # r = db.execute(f"select * from {dict_dbname} where true;\
            #     ").fetchall()
            r = m.get_all_records_of_table(table_name=dict_dbname, columns=columns)
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"error getting words for dict_id {dict_id}")
    ############# POST###DONE
    elif request.method == 'POST':
        r = request.json
        # TODO: verify r (word-class?)
        try:
            # c = db.cursor()
            # c.execute(f"insert into {dict_dbname}( \
            #     id, line, note, description, date_created, last_modified \
            #     ) values (?,?,?,?,?,?)", (
            #         None, r["line"], r["note"], r["description"], 
            #         r["date_created"], r["last_modified"])
            #     )
            # db.commit()
            # r["id"] = c.lastrowid

            # by DB generated w_id will be written in returned json word
            r["date_created"] = datetime.datetime.now()
            inserted_r = m.insert_single_word_record(table_name=dict_dbname, record=r)
            return respSucc(inserted_r)
        except:
            print(traceback.format_exc())
            return respError("Error write word to database")
    ############# PUT###DONE
    elif request.method == 'PUT':
        r = request.json
        # TODO: verify r (word-class?)
        # word_id = r["id"]
        if ("w_id" not in r) or (not r["w_id"].isdigit()):
            return respError(f"Digit word ID w_id not found in payload")
        try:
            # db.execute(f"""update {dict_dbname} \
            #     set line=?, note=?, description=?, date_created=?, last_modified=? \
            #     where id=?
            #     """, (
            #         r["line"], r["note"], r["description"], 
            #         r["date_created"], r["last_modified"], word_id)
            # )
            # db.commit()
            r["last_modified"] = datetime.datetime.now()
            m.update_word_record(table_name=dict_dbname, record=r)
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"Error edit word with id {word_id} in database")

    return respError("unknow error")


@bp.route('/api/v1/dicts/<int:dict_id>/words/<word_id_raw>', 
                    methods=['GET', 'DELETE'])
@auth.login_required
def words_id_handler(dict_id, word_id_raw):
    db = get_db()
    # dict_dbname = getDictTableName(db, dict_id)
    # if not dict_dbname:
    #     return respSucc("dict id not found in database")

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
    query_parameters = request.args
    columns = "*"
    if "columns" in query_parameters:
        columns_raw = query_parameters.get('columns')
        columns = ','.join(c for c in columns_raw.split("."))
    m = custom_model.TB_VocabularyCollection(db, "")
    table_names = m.get_records_with_ids(
        table_name="ALL_DICTS", ids=[dict_id], columns="table_name")
    if len(table_names)==0:
        return respError(f"No dict with id {dict_id} found")
    dict_dbname = table_names[0]["table_name"]
    ############# GET###DONE
    if request.method == 'GET':
        try:
            if word_id:
                # r = db.execute(f"select * from {dict_dbname} where \
                #     id={word_id};").fetchone()
                r = m.get_records_with_ids(table_name=dict_dbname, ids=[word_id_raw], columns=columns)
            else:
                if rand:
                    # r = db.execute(f"select * from {dict_dbname} where \
                    #     rowid=(abs(random()) % (select (select max(rowid) from {dict_dbname}))+1);\
                    #     ").fetchone()
                    random_where = f"rowid=(abs(random()) % (select (select max(rowid) from {dict_dbname}))+1)"
                    r = m.get_records_with_custom_where(
                        table_name=dict_dbname, columns=columns, custom_where=random_where)
                elif top and bot:
                    # r = db.execute(f"SELECT * FROM {dict_dbname} WHERE \
                    #     id between {bot} and {top};\
                    #     ").fetchall()
                    range_where = f"w_id between {bot} and {top}"
                    r = m.get_records_with_custom_where(
                        table_name=dict_dbname, columns=columns, custom_where=range_where)
                else:
                    return respError(f"Request error. Should e")

            if r:
                return respSucc(r)
            else:
                return respError(f"word with id {word_id_raw} not found")
        except:
            print(traceback.format_exc())
            return respError(f"error getting {word_id_raw}")
    ############# DEL###DONE
    elif request.method == 'DELETE':
        if word_id_raw=="":
            return respError("word id not supplied")
        try:
            # db.execute(f"delete from {dict_dbname} where \
            #     id={word_id}")
            # db.commit()
            m.delete_word_record(table_name=dict_dbname, w_id=word_id_raw)
            return respSucc(word_id)
        except:
            print(traceback.format_exc())
            return respError(f"error deleting word id {word_id}")

    return respError("unknow error")

@bp.route('/api/v1/dicts/', methods=['GET', 'POST', 'PUT'])
@auth.login_required
def dicts_handler():
    db = get_db()
    all_dicts = "ALL_DICTS"
    query_parameters = request.args
    columns = "*"
    if "columns" in query_parameters:
        columns_raw = query_parameters.get('columns')
        columns = ','.join(c for c in columns_raw.split("."))
    m = custom_model.TB_VocabularyCollection(db, "")
    # table_names = m.get_records_with_ids(
    #     table_name="ALL_DICTS", ids=[dict_id], columns="table_name")
    # if len(table_names)==0:
    #     return respError(f"No dict with id {dict_id} found")
    # dict_dbname = table_names[0]["table_name"]
    ############# GET
    if request.method == 'GET':
        try:
            # r = db.execute(f"select max(rowid) from {all_dicts};\
            #     ").fetchone()
            # if int(r["max(rowid)"]) > MAX_DB_RANGE:
            s = m.get_size_of_table(table_name=all_dicts)
            if int(s) > MAX_DB_RANGE:
                return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /dicts/1-{MAX_DB_RANGE}")
            # r = db.execute(f"select * from {all_dicts} where true;\
            #     ").fetchall()
            r = m.get_all_records_of_table(table_name=all_dicts, columns=columns)
            return respSucc(r)
        except: 
            print(traceback.format_exc())
            return respError(f"error getting dicts")
    ############# POST
    elif request.method == 'POST':
        r = request.json
        try:
            c = db.cursor()
            c.execute(f"insert into {all_dicts}( \
                w_id, table_name, size \
                ) values (?,?,?)", (None, r["table_name"], r["size"])
            )
            db.commit()
            r["w_id"] = c.lastrowid
            return respSucc(r)
            ####
            # r["date_created"] = datetime.datetime.now()
            # inserted_r = m.create_word_table(table_name=r["table_name"])
            return respSucc(inserted_r)
        except:
            print(traceback.format_exc())
            return respError("Error POST dict to database")
    ############# PUT
    elif request.method == 'PUT':
        r = request.json
        # dict_id = r["id"]
        if ("w_id" not in r) or (not r["w_id"].isdigit()):
            return respError(f"Digit dict ID w_id not found in payload")
        try:
            db.execute(f"""update {all_dicts} \
                set table_name=?, size=?\
                where id=?
                """, (r["table_name"], r["size"], r["w_id"])
            )
            db.commit()
            return respSucc(r)
            # r["last_modified"] = datetime.datetime.now()
            # m.update_word_record(table_name=all_dicts, record=r)
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"Error edit dict with id {dict_id} in database")

    return respError("unknow error")


@bp.route('/api/v1/dicts/<dict_id_raw>', methods=['GET', 'DELETE'])
@auth.login_required
def dicts_id_handler(dict_id_raw):
    db = get_db()
    all_dicts = "ALL_DICTS"
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
            return respError("dict_id must be numberic or range (i.e 123-456)")
        (bot, top) = temp[0]
        if abs(int(top)-int(bot)) > MAX_DB_RANGE:
            return respError(f"DB too big. Break into range {MAX_DB_RANGE}: /words/1-{MAX_DB_RANGE}")
    m = custom_model.TB_VocabularyCollection(db, "")
    query_parameters = request.args
    columns = "*"
    if "columns" in query_parameters:
        columns_raw = query_parameters.get('columns')
        columns = ','.join(c for c in columns_raw.split("."))
    ############# GET###DONE
    if request.method == 'GET':
        try:
            if dict_id:
                # r = db.execute(f"select * from {dict_dbname} where \
                #     id={dict_id};").fetchone()
                r = m.get_records_with_ids(table_name=all_dicts, ids=[dict_id], columns=columns)
            else:
                if rand:
                    #TODO: bug if ALL_DICTS was add/delete before, may return []

                    # r = db.execute(f"select * from {dict_dbname} where \
                    #     rowid=(abs(random()) % (select (select max(rowid) from {dict_dbname}))+1);\
                    #     ").fetchone()
                    r = m.get_records_with_custom_where(table_name=all_dicts, columns=columns,
                        custom_where=f"rowid=(abs(random()) % (select (select max(rowid) from {all_dicts}))+1)")

                elif top and bot:
                    # r = db.execute(f"SELECT * FROM {dict_dbname} WHERE \
                    #     id between {bot} and {top};\
                    #     ").fetchall()
                    r = m.get_records_with_custom_where(table_name=all_dicts, columns=columns,
                        custom_where=f"w_id between {bot} and {top}")
            return respSucc(r)
        except:
            print(traceback.format_exc())
            return respError(f"error getting {dict_id_raw}")
    ############# DEL###DONE
    elif request.method == 'DELETE':
        if not dict_id:
            return respError("dict id not supplied")
        try:
            # db.execute(f"delete from {dict_dbname} where \
            #     id={dict_id}")
            # db.commit()
            #### Get table name:
            table_names = m.get_records_with_ids(
                table_name="ALL_DICTS", ids=[dict_id], columns="table_name"
                )
            if len(table_names)==0:
                return respError(f"No dict with id {dict_id} found")
            m.drop_word_table(table_name=table_names[0]["table_name"])
            return respSucc(dict_id)
        except:
            print(traceback.format_exc())
            return respError(f"error deleting dict id {dict_id}")

    return respError("unknow error")