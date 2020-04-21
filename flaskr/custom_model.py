import sqlite3
import datetime, time
import re
import traceback

def dict_factory_custom(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def construct_record_tuple(records, include_wid=True, wid_none=True, only_exist=False):
    '''
    @param wid_none Set w_id None no matter which value in w_id was supplied
    '''
    r_records = []
    if not only_exist:
        for record in records:
            w_id = None if ("w_id" not in record or wid_none) else record["w_id"]
            word = "" if ("word" not in record) else record["word"]
            gender = "" if ("gender" not in record) else record["gender"]
            w_types = "" if ("w_types" not in record) else record["w_types"]
            features = "" if ("features" not in record) else record["features"]
            also_form = "" if ("also_form" not in record) else record["also_form"]
            long_form = "" if ("long_form" not in record) else record["long_form"]
            plural = "" if ("plural" not in record) else record["plural"]
            past_form = "" if ("past_form" not in record) else record["past_form"]
            pronunciation = "" if ("pronunciation" not in record) else record["pronunciation"]
            meaning = "" if ("meaning" not in record) else record["meaning"]
            tags = "" if ("tags" not in record) else record["tags"]
            antonyms = "" if ("antonyms" not in record) else record["antonyms"]
            synonyms = "" if ("synonyms" not in record) else record["synonyms"]
            raw = "" if ("raw" not in record) else record["raw"]
            note = "" if ("note" not in record) else record["note"]
            description = "" if ("description" not in record) else record["description"]
            date_created = "" if ("date_created" not in record) else record["date_created"]
            last_modified = "" if ("last_modified" not in record) else record["last_modified"]
            if include_wid:
                # for example UPDATE query no need for w_id
                r_records.append((w_id, word, gender, w_types, features, also_form, long_form, plural,
                    past_form, pronunciation, meaning, tags, antonyms, synonyms,
                    raw, note, description, date_created, last_modified))
            else:
                r_records.append((word, gender, w_types, features, also_form, long_form, plural,
                    past_form, pronunciation, meaning, tags, antonyms, synonyms,
                    raw, note, description, date_created, last_modified))
    else:
        for record in records:
            r_record = []
            if include_wid:
                if ("w_id" in record):
                    if not wid_none:
                        r_record.append(record["w_id"])
                    else: 
                        r_record.append(None)
            if ("word"  in record): 
                r_record.append(record["word"])
            if ("gender"  in record): 
                r_record.append(record["gender"])
            if ("w_types"  in record): 
                r_record.append(record["w_types"])
            if ("features"  in record): 
                r_record.append(record["features"])
            if ("also_form"  in record): 
                r_record.append(record["also_form"])
            if ("long_form"  in record): 
                r_record.append(record["long_form"])
            if ("plural"  in record): 
                r_record.append(record["plural"])
            if ("past_form"  in record): 
                r_record.append(record["past_form"])
            if ("pronunciation"  in record): 
                r_record.append(record["pronunciation"])
            if ("meaning"  in record): 
                r_record.append(record["meaning"])
            if ("tags"  in record): 
                r_record.append(record["tags"])
            if ("antonyms"  in record): 
                r_record.append(record["antonyms"])
            if ("synonyms"  in record): 
                r_record.append(record["synonyms"])
            if ("raw"  in record): 
                r_record.append(record["raw"])
            if ("note"  in record): 
                r_record.append(record["note"])
            if ("description"  in record): 
                r_record.append(record["description"])
            if ("date_created"  in record): 
                r_record.append(record["date_created"])
            if ("last_modified"  in record): 
                r_record.append(record["last_modified"])
            r_records.append(r_record)
    return r_records

def construct_record_place_holder(record):
    r_record = ""
    if ("word"  in record): 
        r_record += f"word=?,"
    if ("gender"  in record): 
        r_record += f"gender=?,"
    if ("w_types"  in record): 
        r_record += f"w_types=?,"
    if ("features"  in record): 
        r_record += f"features=?,"
    if ("also_form"  in record): 
        r_record += f"also_form=?,"
    if ("long_form"  in record): 
        r_record += f"long_form=?,"
    if ("plural"  in record): 
        r_record += f"plural=?,"
    if ("past_form"  in record): 
        r_record += f"past_form=?,"
    if ("pronunciation"  in record): 
        r_record += f"pronunciation=?,"
    if ("meaning"  in record): 
        r_record += f"meaning=?,"
    if ("tags"  in record): 
        r_record += f"tags=?,"
    if ("antonyms"  in record): 
        r_record += f"antonyms=?,"
    if ("synonyms"  in record): 
        r_record += f"synonyms=?,"
    if ("raw"  in record): 
        r_record += f"raw=?,"
    if ("note"  in record): 
        r_record += f"note=?,"
    if ("description"  in record): 
        r_record += f"description=?,"
    if ("date_created"  in record): 
        r_record += f"date_created=?,"
    if ("last_modified"  in record): 
        r_record += f"last_modified=?,"
    return r_record[:-1]

class TB_VocabularyCollection:
    def __init__(self, db, tableName=""):
        self.db = db
        self.tableName = tableName

    def get_size_of_table(self, table_name=""):
        table_name = self.tableName if (table_name=="") else table_name
        ##
        r = self.db.execute(f"select max(rowid) from {table_name};").fetchone()
        return int(r["max(rowid)"])

    def get_all_records_of_table(self, table_name="", columns=""):
        table_name = self.tableName if (table_name=="") else table_name
        columns = "*" if (columns=="") else columns
        ##
        r = self.db.execute(f"select {columns} from {table_name} where true;").fetchall()
        return r

    def get_records_with_ids(self, table_name="", ids=[], columns=""):
        '''
        @param columns Specify which column to be SELECT. i.e: columns="w_id, table_name"
        '''
        ''' Example
        print(m.get_records_with_ids(table_name="ALL_DICTS", ids=[1]))
        => [{'w_id': 1, 'table_name': 'DE_EN', 'size': 1206750}]
        '''
        table_name = self.tableName if (table_name=="") else table_name
        columns = "*" if (columns=="") else columns
        ##
        ph = ','.join("?" for i in range(0,len(ids)))
        r = self.db.execute(f"select {columns} from {table_name} where w_id in ({ph});", tuple(ids)).fetchall()
        return r

    def get_records_with_custom_where(self, table_name="", columns="", custom_where=""):
        ''' D
        @param custom_where Custom string to put behind 'WHERE'. ';' added by this method.
        '''
        table_name = self.tableName if (table_name=="") else table_name
        columns = "*" if (columns=="") else columns
        ##
        r = self.db.execute(f"select {columns} from {table_name} where {custom_where};").fetchall()
        return r

    def get_records_with_ids_in_range(self, table_name="", ids=[], columns=""):
        table_name = self.tableName if (table_name=="") else table_name
        columns = "*" if (columns=="") else columns
        ##
        r = self.db.execute(f"select {columns} from {table_name} where w_id between {ids[0]} and {ids[1]};").fetchall()
        return r

    # SELECT *,"EN_DE" as table_name FROM EN_DE where word like "engi%"
    # UNION
    # SELECT *,"EN_FR" as table_name FROM EN_FR where word like "engi%"
    # UNION
    # SELECT *,"DE_EN" as table_name FROM DE_EN where word like "engi%"
    # UNION
    # SELECT *,"DE_FR" as table_name FROM DE_FR where word like "engi%"
    # UNION
    # SELECT *,"FR_EN" as table_name FROM FR_EN where word like "engi%"
    # UNION
    # SELECT *,"FR_DE" as table_name FROM FR_DE where word like "engi%"
    def search_record_by_word(self, table_names=[""], select_what="*", keyword=""):
        query = ""
        if len(table_names) == 1:
            query +=    f"SELECT {select_what} FROM {table_names[0]}" + \
                        f" WHERE word LIKE \"{keyword}\""
        else:
            for table_name in table_names:
                query +=    f"SELECT {select_what}, \"{table_name}\" AS table_name FROM {table_name}" + \
                            f" WHERE word LIKE \"{keyword}\" UNION "
            query = query[:-7] + ";"    # ' UNION '
        print(query)
        r = self.db.execute(query).fetchall()
        return r

    def insert_word_records(self, table_name="", records=[]):
        table_name = self.tableName if (table_name=="") else table_name
        querry = f"insert into {table_name}\
        (w_id, word, gender, w_types, features, also_form, long_form, plural, \
        past_form, pronunciation, meaning, tags, antonyms, synonyms, \
        raw, note, description, date_created, last_modified) \
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        values = construct_record_tuple(records, include_wid=True, wid_none=True)
        self.db.executemany(querry, values)
        self.db.commit()

    def insert_single_word_record(self, table_name="", record={}):
        table_name = self.tableName if (table_name=="") else table_name
        querry = f"insert into {table_name}\
        (w_id, word, gender, w_types, features, also_form, long_form, plural, \
        past_form, pronunciation, meaning, tags, antonyms, synonyms, \
        raw, note, description, date_created, last_modified) \
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        # construct_record_tuple written for multiple words in mind, so lets convert it to list
        # w_id for insert will be set to None (because of AUTOINCREMENT)
        value = construct_record_tuple([record], include_wid=True, wid_none=True)[0]
        c = self.db.cursor()
        c.execute(querry, value)
        # self.db.execute(querry, value)
        self.db.commit()
        record["w_id"] = str(c.lastrowid)
        return record
    
    def update_word_record(self, table_name="", record={}):
        table_name = self.tableName if (table_name=="") else table_name
        w_id = record["w_id"]
        querry = f"UPDATE {table_name}\
            SET {construct_record_place_holder(record)}\
            WHERE w_id=\"{str(w_id)}\""
        values = tuple(construct_record_tuple([record], include_wid=False, only_exist=True)[0])
        self.db.execute(querry, values)
        self.db.commit()

    def delete_word_record(self, table_name="", w_id=""):
        table_name = self.tableName if (table_name=="") else table_name
        querry = f"DELETE FROM {table_name} WHERE w_id=\"{str(w_id)}\""
        self.db.execute(querry)
        self.db.commit()

    def create_word_table(self, table_name):
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name}( \
            w_id INTEGER PRIMARY KEY AUTOINCREMENT, \
            word TEXT NOT NULL, gender TEXT, w_types TEXT,\
            features TEXT, also_form TEXT, long_form TEXT,\
            plural TEXT, past_form TEXT, pronunciation TEXT,\
            meaning TEXT, tags TEXT, antonyms TEXT,\
            synonyms TEXT, raw TEXT, note TEXT, \
            description TEXT, date_created timestamp, last_modified timestamp \
            )")
        self.db.commit()
        self.db.execute(f"INSERT INTO ALL_DICTS (table_name) VALUES (\"{table_name}\")")
        self.db.commit()
        ##
        # c = self.db.cursor()
        # c.execute(querry, value)
        # # self.db.execute(querry, value)
        # self.db.commit()
        # record["w_id"] = str(c.lastrowid)
        # return record

    def drop_word_table(self, table_name):
        self.db.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.db.commit()
        self.db.execute(f"DELETE FROM ALL_DICTS WHERE table_name=\"{table_name}\"")
        self.db.commit()

# m = TB_VocabularyCollection(con, "")
# print(m.get_all_records_of_table("ALL_DICTS"))
# print(m.get_size_of_table("DE_EN"))
# print(m.get_records_with_ids("DE_EN", [1,2,3,4], "w_id, word"))
# print(m.get_records_with_ids_in_range("DE_EN", [1,2,3,4], "w_id, word"))

# records=[{"w_id":1, "word": "tada"}, {"w_id":3, "word": "tada3"}]
# record = {"w_id":1, "word": "tada2222222222"}

### Test addd
# try:
#     m.create_word_table("test_table")
#     m.insert_word_records(table_name="test_table", records=records)
# except:
#     print(traceback.format_exc())

# Test drop
# try:
#     m.drop_word_table("test_table")
# except:
#     print(traceback.format_exc())

### Test delete
# try:
#     m.delete_word_record(table_name="test_table", record=record)
# except:
#     print(traceback.format_exc())
# print(construct_record_place_holder(record))
# print(tuple(construct_record_tuple([record], include_wid=False, only_exist=True)[0]))


# try:
    # print(m.search_record_by_word(table_names=["EN_DE", "EN_FR", "DE_FR", "DE_EN", "FR_DE", "FR_EN"], keyword="%test%"))
#     print(m.search_record_by_word(select_what="w_id", table_names=["EN_DE", "EN_FR", "DE_FR", "DE_EN", "FR_DE", "FR_EN"], keyword="%test%"))
# except:
#     print(traceback.format_exc())

