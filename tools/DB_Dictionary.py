import sqlite3
from sqlite3 import Error


def initTablesForDBDictionary(conn):
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS tb_Language (ID INTEGER PRIMARY KEY AUTOINCREMENT,Language	TEXT)""")
    conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Sample_Sentence (
        ID	INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Vocabulary_Denotation	INTEGER,
        Sentence	TEXT,
        Translated_Sentence	TEXT,
        Writer	TEXT,
        Date	TEXT
        )""")
    conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Vocabulary (
        ID	INTEGER PRIMARY KEY AUTOINCREMENT,
        Vocabulary	TEXT,
        ID_Language	INTEGER
        )""")
    conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Vocabulary_Denotation (
        ID	INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Vocabulary	INTEGER,
        Type	TEXT,
        ID_Language	INTEGER,
        Meaning	TEXT,
        Tags TEXT
        )""")


class DB_SqliteDictionary:
    def __init__(self, db_File):
        self.db_File = db_File

    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_File)
            initTablesForDBDictionary(conn)
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
class TB_LanguageRecord:
    ID = "ID"
    Language = "Language"

    def __init__(self, id, language):
        self.id = id
        self.language = language

    def toTupel(self):
        return self.id, self.language

    def toJson(self):
        return "{" + f""" "{TB_LanguageRecord.ID}":{self.id},"{TB_LanguageRecord.Language}":"{self.language}" """ + "}"


# -------------------------------------------------------------------------------------------------------------------#
class TB_LanguageCollection:
    def __init__(self, conn, tableName="tb_Language"):
        self.conn = conn
        self.tableName = tableName

    def getRecordByID(self, id):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {self.tableName} WHERE {TB_LanguageRecord.ID}={id}"""
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            record = TB_LanguageRecord(row[0], row[1])
            return record
        else:
            return None

    def insertRecord(self, record):
        sql = f"""INSERT INTO {self.tableName}({TB_LanguageRecord.ID},{TB_LanguageRecord.Language})
              VALUES(?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, record.toTupel())
        return cur.lastrowid

    def removeRecordByID(self, record):
        sql = f"""DELETE FROM {self.tableName} WHERE {TB_LanguageRecord.ID} ={record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def updateRecordByID(self, record):
        sql = f"""UPDATE {self.tableName} SET {TB_LanguageRecord.Language} = {record.language} WHERE {TB_LanguageRecord.ID} = {record.id}"""
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
        query = f"SELECT * FROM {self.tableName} WHERE {condition}"
        cur.execute(query)
        rows = cur.fetchall()
        records = []
        for row in rows:
            record = TB_LanguageRecord(row[0], row[1])
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


####################################################################################################################
class TB_SampleSentenceRecord:
    ID = "ID"
    ID_Vocabulary_Denotation = "ID_Vocabulary_Denotation"
    Sentence = "Sentence"
    Translated_Sentence = "Translated_Sentence"
    Writer = "Writer"
    Date = "Date"

    def __init__(self, id, idVocabularyDenotation, sentence, translatedSentence, writer, date):
        self.id = id
        self.idVocabularyDenotation = idVocabularyDenotation
        self.sentence = sentence
        self.translatedSentence = translatedSentence
        self.writer = writer
        self.date = date

    def toTupel(self):
        return self.id, self.idVocabularyDenotation, self.sentence, self.translatedSentence, self.writer, self.date

    def toJson(self):
        return "{" + f""" "{TB_SampleSentenceRecord.ID}": {self.id},"{TB_SampleSentenceRecord.ID_Vocabulary_Denotation}":{self.idVocabularyDenotation}
,"{TB_SampleSentenceRecord.Sentence}":"{self.sentence}","{TB_SampleSentenceRecord.Translated_Sentence}":"{self.translatedSentence}"
,"{TB_SampleSentenceRecord.Writer}":"{self.Writer}","{TB_SampleSentenceRecord.Date}":"{self.date}" """ + "}"


# -------------------------------------------------------------------------------------------------------------------#
class TB_SampleSentenceCollection:
    def __init__(self, conn, tableName="tb_Sample_Sentence"):
        self.conn = conn
        self.tableName = tableName

    def getRecordByID(self, id):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {self.tableName} WHERE {TB_SampleSentenceRecord.ID}={id}"""
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            record = TB_SampleSentenceRecord(row[0], row[1], row[2], row[3], row[4], row[5])
            return record
        else:
            return None

    def insertRecord(self, record):
        sql = f"""INSERT INTO {self.tableName} ({TB_SampleSentenceRecord.ID},{TB_SampleSentenceRecord.ID_Vocabulary_Denotation},{TB_SampleSentenceRecord.Sentence},{TB_SampleSentenceRecord.Translated_Sentence},{TB_SampleSentenceRecord.Writer},{TB_SampleSentenceRecord.Date})
              VALUES(?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, record.toTupel())
        return cur.lastrowid

    def removeRecordByID(self, record):
        sql = f"""DELETE FROM {self.tableName} WHERE {TB_SampleSentenceRecord.ID} ={record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def updateRecordByID(self, record):
        sql = f"""UPDATE {self.tableName} SET {TB_SampleSentenceRecord.ID_Vocabulary_Denotation}={record.idVocabularyDenotation},{TB_SampleSentenceRecord.Sentence}={record.sentence},{TB_SampleSentenceRecord.Translated_Sentence}={record.translatedSentence},{TB_SampleSentenceRecord.Writer}={record.writer},{TB_SampleSentenceRecord.Date}={record.date} WHERE {TB_SampleSentenceRecord.ID} = {record.id}"""
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
            record = TB_SampleSentenceRecord(row[0], row[1], row[2], row[3], row[4], row[5])
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


####################################################################################################################
class TB_VocabularyRecord:
    ID = "ID"
    Vocabulary = "Vocabulary"
    ID_Language = "ID_Language"

    def __init__(self, id, vocabulary, idLanguage):
        self.id = id
        self.vocabulary = vocabulary
        self.idLanguage = idLanguage

    def toTupel(self):
        return self.id, self.vocabulary, self.idLanguage

    def toJson(self):
        return "{"+f""" "{TB_VocabularyRecord.ID}":{self.id},"{TB_VocabularyRecord.Vocabulary}":"{self.vocabulary}"
        ,"{TB_VocabularyRecord.ID_Language}":{self.idLanguage} """+"}"
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
            record = TB_VocabularyRecord(row[0], row[1], row[2])
            return record
        else:
            return None

    def insertRecord(self, record):
        sql = f"""INSERT INTO {self.tableName}({TB_VocabularyRecord.ID},{TB_VocabularyRecord.Vocabulary},{TB_VocabularyRecord.ID_Language})
              VALUES(?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, record.toTupel())
        return cur.lastrowid

    def removeRecordByID(self, record):
        sql = f"""DELETE FROM {self.tableName} WHERE {TB_VocabularyRecord.ID} ={record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def updateRecordByID(self, record):
        sql = f"""UPDATE {self.tableName} SET {TB_VocabularyRecord.Vocabulary}={record.vocabulary}, {TB_VocabularyRecord.ID_Language}={record.idLanguage} WHERE {TB_VocabularyRecord.ID} = {record.id}"""
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
            record = TB_VocabularyRecord(row[0], row[1], row[2])
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


####################################################################################################################
class TB_VocabularyDenotationRecord:
    ID = "ID"
    ID_Vocabulary = "ID_Vocabulary"
    Type = "Type"
    ID_Language = "ID_Language"
    Meaning = "Meaning"
    Tags = "Tags"

    def __init__(self, id, idVocabulary, type, idLanguage, meaning, tags):
        self.id = id
        self.idVocabulary = idVocabulary
        self.type = type
        self.idLanguage = idLanguage
        self.meaning = meaning
        self.tags = tags

    def toTupel(self):
        return self.id, self.idVocabulary, self.type, self.idLanguage, self.meaning, self.tags

    def toJson(self):
        return "{"+f""" "{TB_VocabularyDenotationRecord.ID}":{self.id},"{TB_VocabularyDenotationRecord.ID_Vocabulary}":{self.idVocabulary}
,"{TB_VocabularyDenotationRecord.Type}":"{self.type}","{TB_VocabularyDenotationRecord.ID_Language}":{self.idLanguage}
,"{TB_VocabularyDenotationRecord.Meaning}":"{self.meaning}","{TB_VocabularyDenotationRecord.Tags}":"{self.tags}" """+"}"


# -------------------------------------------------------------------------------------------------------------------#
class TB_VocabularyDenotationCollection:
    def __init__(self, conn, tableName="tb_Vocabulary_Denotation"):
        self.conn = conn
        self.tableName = tableName

    def getRecordByID(self, id):
        cur = self.conn.cursor()
        query = f"""SELECT * FROM {self.tableName} WHERE id={id}"""
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            record = TB_VocabularyDenotationRecord(row[0], row[1], row[2], row[3], row[4], row[5])
            return record
        else:
            return None

    def insertRecord(self, record):
        sql = f"""INSERT INTO {self.tableName}({TB_VocabularyDenotationRecord.ID},{TB_VocabularyDenotationRecord.ID_Vocabulary},{TB_VocabularyDenotationRecord.Type},{TB_VocabularyDenotationRecord.ID_Language},{TB_VocabularyDenotationRecord.Meaning},{TB_VocabularyDenotationRecord.Tags})
              VALUES(?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, record.toTupel())
        return cur.rowcount

    def removeRecordByID(self, record):
        sql = f"""DELETE FROM {self.tableName} WHERE ID ={record.id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.rowcount

    def updateRecordByID(self, record):
        sql = f"""UPDATE {self.tableName} SET {TB_VocabularyDenotationRecord.ID_Vocabulary}={record.idVocabulary},{TB_VocabularyDenotationRecord.Type}="{record.type}",{TB_VocabularyDenotationRecord.ID_Language}={record.idLanguage},{TB_VocabularyDenotationRecord.Meaning}="{record.meaning}",{TB_VocabularyDenotationRecord.Tags}="{record.tags}" WHERE {TB_VocabularyDenotationRecord.ID} = {record.id}"""
        cur = self.conn.cursor()
        print(sql)
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
            record = TB_VocabularyDenotationRecord(row[0], row[1], row[2], row[3], row[4],row[5])
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
