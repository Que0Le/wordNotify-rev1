import sqlite3
from sqlite3 import Error


def initTablesForDBDictionary(conn, tableName="tb_Vocabulary"):
    conn.execute(f"""CREATE TABLE IF NOT EXISTS {tableName} (
        ID	INTEGER PRIMARY KEY AUTOINCREMENT,
        Vocabulary	TEXT,
        Meaning	TEXT,
        Types TEXT,
        Tags TEXT
        )""")


class DB_SqliteDictionary:
    def __init__(self, db_File):
        self.db_File = db_File

    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_File)
            #initTablesForDBDictionary(conn)
        except Error as e:
            print(e)
        return conn


class QueryExecuter:
    def __init__(self, conn):
        self.conn = conn

    def executeDataQuery(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def executeActionQuery(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.rowcount


####################################################################################################################
class TB_VocabularyRecord:
    ID = "ID"
    Vocabulary = "Vocabulary"
    Meaning = "Meaning"
    Types = "Types"
    Tags = "Tags"

    def __init__(self, id, vocabulary, meaning, types, tags):
        self.id = id
        self.vocabulary = vocabulary
        self.meaning = meaning
        self.types = types
        self.tags = tags

    def toTupel(self):
        return self.id, self.vocabulary, self.meaning, self.types, self.tags

    def toJson(self):
        return "{" + f""" "{TB_VocabularyRecord.ID}":{self.id},"{TB_VocabularyRecord.Vocabulary}":"{self.vocabulary}"
        ,"{TB_VocabularyRecord.Meaning}":"{self.meaning}","{TB_VocabularyRecord.Types}":"{self.types}", "{TB_VocabularyRecord.Tags}":"{self.tags}" """ + "}"


# -------------------------------------------------------------------------------------------------------------------#

class TB_VocabularyCollection:
    def __init__(self, conn, tableName="tb_Vocabulary"):
        self.conn = conn
        self.tableName = tableName

    def getRecordByID(self, id):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {self.tableName} WHERE {TB_VocabularyRecord.ID}={id}"""
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            record = TB_VocabularyRecord(row[0], row[1], row[2], row[3], row[4])
            return record
        else:
            return None

    def insertRecord(self, record):
        sql = f"""INSERT INTO {self.tableName}({TB_VocabularyRecord.ID},{TB_VocabularyRecord.Vocabulary},{TB_VocabularyRecord.Meaning},{TB_VocabularyRecord.Types},{TB_VocabularyRecord.Tags})
              VALUES(?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, record.toTupel())
        return cur.lastrowid

    def removeRecordByID(self, record):
        sql = f"""DELETE FROM {self.tableName} WHERE {TB_VocabularyRecord.ID} ={record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def updateRecordByID(self, record):
        sql = f"""UPDATE {self.tableName} SET {TB_VocabularyRecord.Vocabulary}="{record.vocabulary}", {TB_VocabularyRecord.Meaning}="{record.meaning}",{TB_VocabularyRecord.Types}="{record.types}", {TB_VocabularyRecord.Tags}="{record.tags}" WHERE {TB_VocabularyRecord.ID} = {record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def insertCollection(self, collection):
        rowcount = 0
        for record in collection:
            rowcount = rowcount + self.insertRecord(record)
        return rowcount

    def removeCollection(self, collection):
        rowcount = 0
        for record in collection:
            rowcount = rowcount + self.removeRecordByID(record)
        return rowcount

    def updateCollection(self, collection):
        rowcount = 0
        for record in collection:
            rowcount = rowcount + self.updateRecordByID(record)
        return rowcount

    def getDataByCondition(self, condition="1=1"):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {self.tableName} WHERE {condition}"""
        cur.execute(query)
        rows = cur.fetchall()
        records = []
        for row in rows:
            record = TB_VocabularyRecord(row[0], row[1], row[2],row[3], row[4])
            records.append(record)
        return records

    def updateDataByCondition(self, feld, condition):
        sql = f"""UPDATE {self.tableName} SET {feld} WHERE {condition}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def removeDataByCondition(self, condition):
        sql = f"""DELETE FROM {self.tableName} WHERE {condition}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount
