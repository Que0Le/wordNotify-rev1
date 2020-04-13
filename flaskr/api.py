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
            handyfunctions.update_config(current_app, new_config)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": error})

@bp.route('/api/v1/resources/dicts_db', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def api_dicts_db():
    db = get_db()
    r = request.json
    if request.method == 'GET':
        try:
            all_dicts = db.execute(
                "SELECT * FROM ALL_DICTS;"
                ).fetchall()
            return jsonify(all_dicts)
        except Exception:
            print(traceback.format_exc())
            return jsonify({"status": "GET DB error"})
    elif request.method == 'POST':
        try:
            db.execute("insert into ALL_DICTS (table_name) \
                    values (?);", r["dict_db"])
            db.commit()
            return r
        except Exception:
            print(traceback.format_exc())
            return jsonify({"status": "POST DB error"})

    elif request.method == 'PUT':
        try:
            db.execute("update ALL_DICTS set table_name=? where table_name=?;\
                ", (r["new_dict_db"], r["dict_db"])).fetchall()
            db.commit()
            return r
        except Exception:
            print(traceback.format_exc())
            return jsonify({"status": "PUT DB error"})
    elif request.method == 'DELETE':
        try:
            db.execute("delete from ALL_DICTS where\
                    table_name=;\
                ", r["dict_db"]).fetchall()
            db.commit()
            return r
        except Exception:
            print(traceback.format_exc())
            return jsonify({"status": "DELETE DB error"})

@bp.route('/api/v1/resources/dicts', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def api_filter():
    query_parameters = request.args

    dict_db = query_parameters.get('dict_db')
    if dict_db:
        # url mode http://127.0.0.1:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
        id = query_parameters.get('id')
        rand = query_parameters.get('random')
        if not (dict_db!= "" and (rand or id)):
            return page_not_found(404)

        if request.method == 'GET':
            query = f"SELECT * FROM {dict_db} WHERE"

            if rand=="true":
                # select * from DE_EN where rowid = (abs(random()) % (select (select max(rowid) from DE_EN)+1));
                query += f' rowid=(abs(random()) % (select (select max(rowid) from {dict_db}))+1) AND'
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
    else:
        # Payload mode
        ###############
        db = get_db()
        ########################################## GET
        if request.method == 'GET':
            r_dicts = request.json
            response = []
            for r_dict in r_dicts:
                # DE_EN
                dict_db = r_dict["dict_db"]
                option = r_dict["option"]
                ids = r_dict["ids"]
                id_ranges = r_dict["id_ranges"]
                id_random = r_dict["id_random"]
                response_ids = []
                response_ranges = {}
                response_random = []
                response_all = []
                if option=="all":
                    try:
                        response_all = db.execute(f"""\
                            SELECT * FROM {r_dict["dict_db"]} WHERE true;\
                            """).fetchall()
                    except:
                        print(traceback.format_exc())
                # Get words with ids
                try:
                    place_holders = ', '.join(['?']*len(ids)) # ','.join(map(str, ids))
                    response_ids = db.execute(f"""\
                        SELECT * FROM {r_dict["dict_db"]} WHERE \
                        id in ({place_holders}); \
                        """, tuple(ids)).fetchall()
                except Exception:
                    print(traceback.format_exc())
                # Get word has id in range defined in id_ranges. 
                try:
                    for range_id_string in id_ranges:
                        temp = re.findall(r"([0-9]+)-([0-9]+)", range_id_string)
                        if len(temp) == 0:
                            continue
                        (top, bot) = temp[0]
                        r = db.execute(f"""\
                            SELECT * FROM {r_dict["dict_db"]} WHERE \
                            id between {int(top)} and {int(bot)}; \
                            """).fetchall()
                        response_ranges[range_id_string] = r
                except Exception:
                    print(traceback.format_exc())
                # Get id_random random rows
                try:
                    maxrow = db.execute("select max(rowid) from DE_EN;").fetchone()["max(rowid)"]
                    where_statement = ""
                    if maxrow>id_random:
                        # generate some random ids
                        def random_gen(low, high):
                            while True:
                                yield random.randrange(low, high)
                        gen = random_gen(1, maxrow)
                        temp_ids = set()
                        for x in itertools.takewhile(lambda x: len(temp_ids) < id_random, gen):
                            temp_ids.add(x)
                        # 
                        place_holders = ', '.join(['?']*id_random)
                        response_random = db.execute(f"""\
                            SELECT * FROM {r_dict["dict_db"]} WHERE \
                            id in ({place_holders}); \
                            """, tuple(temp_ids)).fetchall()
                    else:
                        response_random = db.execute(f"""\
                            SELECT * FROM {r_dict["dict_db"]} WHERE true\
                            """).fetchall()
                except Exception:
                    print(traceback.format_exc())
                ####
                #### Construct part of response message
                response_for_single_dict = {
                    "dict_db": dict_db,
                    "ids": response_ids,
                    "id_ranges": response_ranges,
                    "id_random": response_random,
                    "all": response_all
                }
                response.append(response_for_single_dict)
            return jsonify(response)
        ########################################## POST
        elif request.method == 'POST':
            # DE_EN
            req_dicts = request.json
            response = []
            for req_dict in req_dicts:
                dict_db = req_dict["dict_db"]
                data = req_dict["data"]
                posted_words = []
                error_trans = []
                for word in data:
                    try:
                        db.execute(f"insert into {dict_db}( \
                            id, line, note, description, date_created, last_modified \
                            ) values (?,?,?,?,?,?)", (
                                None, word["line"], word["note"], word["description"], 
                                word["date_created"], word["last_modified"])
                            )
                        db.commit()
                        posted_words.append(word)
                    except:
                        error_trans.append(word)
                        print(traceback.format_exc())
                response.append({
                    "dict_db": dict_db, "posted_words": posted_words, "error_trans": error_trans
                    })
            return jsonify(response)


            # req_dicts = request.json
            # for req_dict in req_dicts:
            #     dict_db = req_dict["dict_db"]
            #     data = req_dict["data"]

            #     querry = f"insert into {dict_db}( \
            #         id, line, note, description, date_created, last_modified \
            #         ) values (?,?,?,?,?,?)"
            #     i = 1
            #     data_array = []
            #     try:
            #         for word in data:
            #             data_array.append(
            #                 (None, word["line"], word["note"], word["description"], 
            #                 word["date_created"], word["last_modified"]))
            #             if i%10000 == 0:
            #                 db.executemany(querry, data_array)
            #                 db.commit()
            #                 data_array.clear()
            #             i+=1
            #         db.executemany(querry, data_array)
            #         db.commit()
            #     except:
            #         print(traceback.format_exc())
            #         return jsonify({"status": "Error POST: writing to DB"})
            # return jsonify({"status": "ok"})
        ########################################## POST
        elif request.method == 'PUT':
            # DE_EN
            req_dicts = request.json
            print(req_dicts)
            response = []
            for req_dict in req_dicts:
                dict_db = req_dict["dict_db"]
                data = req_dict["data"]
                updated_words = []
                error_trans = []
                for word in data:
                    try:
                        db.execute(f"""update {dict_db} \
                            set line=?, note=?, description=?, date_created=?, last_modified=? \
                            where id=?
                            """, (
                                word["line"], word["note"], word["description"], 
                                word["date_created"], word["last_modified"], word["id"])
                        )
                        db.commit()
                        updated_words.append(word)
                    except:
                        error_trans.append(word)
                        print(traceback.format_exc())
                response.append({
                    "dict_db": dict_db, "updated_words": updated_words, "error_trans": error_trans
                    })
            return jsonify(response)
        ########################################## DELETE
        elif request.method == 'DELETE':
            # DE_EN
            req_dicts = request.json
            response = []
            for req_dict in req_dicts:
                dict_db = req_dict["dict_db"]
                ids = req_dict["ids"]
                deleted_words = []
                error_trans = []
                for id_single in ids:
                    try:
                        db.execute(f"""delete from {dict_db} where \
                            id={id_single}""")
                        db.commit()
                        deleted_words.append(id_single)
                    except:
                        error_trans.append(id_single)
                        print(traceback.format_exc())
                response.append({
                    "dict_db": dict_db, "deleted_words": deleted_words, "error_trans": error_trans
                    })
            return jsonify(response)
            # req_dicts = request.json
            # for req_dict in req_dicts:
            #     dict_db = req_dict["dict_db"]
            #     ids = req_dict["ids"]
            #     try:
            #         db.execute(f"""delete from {dict_db} where \
            #             id in ({tuple(ids)})""")
            #     except:
            #         print(traceback.format_exc())
            #         return jsonify({"status": "Error POST: writing to DB"})
            # return jsonify({"status": "ok"})




def respError(mess):
    return jsonify({"response": mess, "status": "error"})
def respSucc(mess):
    return jsonify({"response": mess, "status": "success"})

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
        # TODO: But too large DB will break sending back
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
###
###
###
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