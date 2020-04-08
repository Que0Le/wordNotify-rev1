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
	conn.execute(f"""CREATE TABLE tb_Tag (
		ID	INTEGER PRIMARY KEY AUTOINCREMENT,
		Tag	TEXT,
		ID_Language	INTEGER
		)""")
	conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Type (ID	INTEGER PRIMARY KEY AUTOINCREMENT,Type	TEXT)""")
	conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Vocabulary (
		ID	INTEGER PRIMARY KEY AUTOINCREMENT,
		Vocabulary	TEXT,
		ID_Language	INTEGER
		)""")
	conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Vocabulary_Denotation (
		ID	INTEGER PRIMARY KEY AUTOINCREMENT,
		ID_Vocabulary	INTEGER,
		ID_Vocabulary_Type	INTEGER,
		ID_Language	INTEGER,
		Meaning	TEXT)""")
	conn.execute(f"""CREATE TABLE IF NOT EXISTS tb_Vocabulary_Denotation_Tag (
		ID	INTEGER PRIMARY KEY AUTOINCREMENT,
		ID_Vocabulary_Denotation	INTEGER,
		ID_Tag	INTEGER
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


####################################################################################################################
class TB_LanguageRecord:
	def __init__(self, id, language):
		self.id = id
		self.language = language

	def toTupel(self):
		return self.id, self.language


# -------------------------------------------------------------------------------------------------------------------#
class TB_LanguageCollection:
	def __init__(self, conn, tableName="tb_Language"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_LanguageRecord(row[0], row[1])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,Language)
			  VALUES(?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET Language = {1} WHERE ID = {2}""".format(self.tableName, record.language, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = "SELECT * FROM {0} WHERE {1}".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_LanguageRecord(row[0], row[1])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################	
class TB_SampleSentenceRecord:
	def __init__(self, id, idVocabularyDenotation, sentence, translatedSentence, writer, date):
		self.id = id
		self.idVocabularyDenotation = idVocabularyDenotation
		self.sentence = sentence
		self.translatedSentence = translatedSentence
		self.writer = writer
		self.date = date

	def toTupel(self):
		return self.id, self.idVocabularyDenotation, self.sentence, self.translatedSentence, self.writer, self.date


# -------------------------------------------------------------------------------------------------------------------#
class TB_SampleSentenceCollection:
	def __init__(self, conn, tableName="tb_Sample_Sentence"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_SampleSentenceRecord(row[0], row[1], row[2], row[3], row[4], row[5])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,ID_Vocabulary_Denotation,Sentence,Translated_Sentence,Writer,Date)
			  VALUES(?,?,?,?,?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET ID_Vocabulary_Denotation={1},Sentence={2},Translated_Sentence={3},Writer={4},Date={5} WHERE ID = {6}""".format(
			self.tableName, record.idVocabularyDenotation, record.sentence, record.translatedSentence, record.writer,
			record.date, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_SampleSentenceRecord(row[0], row[1], row[2], row[3], row[4], row[5])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################	
class TB_TagRecord:
	def __init__(self, id, tag, idLanguage):
		self.id = id
		self.tag = tag
		self.idLanguage = idLanguage

	def toTupel(self):
		return self.id, self.tag, self.idLanguage


# -------------------------------------------------------------------------------------------------------------------#
class TB_TagCollection:
	def __init__(self, conn, tableName="tb_Tag"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_TagRecord(row[0], row[1], row[2])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,Tag,ID_Language)
			  VALUES(?,?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET Tag={1}, ID_Language={2} WHERE ID = {3}""".format(self.tableName, record.tag,
																				  record.idLanguage, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_TagRecord(row[0], row[1], row[2])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################
class TB_TypeRecord:
	def __init__(self, id, type):
		self.id = id
		self.type = type

	def toTupel(self):
		return self.id, self.type


# -------------------------------------------------------------------------------------------------------------------#
class TB_TypeCollection:
	def __init__(self, conn, tableName="tb_Type"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_TypeRecord(row[0], row[1])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,Type)
			  VALUES(?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET Type={1} WHERE ID = {2}""".format(self.tableName, record.type, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)

		cur.execute(query)

		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_TypeRecord(row[0], row[1])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################
class TB_VocabularyRecord:
	def __init__(self, id, vocabulary, idLanguage):
		self.id = id
		self.vocabulary = vocabulary
		self.idLanguage = idLanguage

	def toTupel(self):
		return self.id, self.vocabulary, self.idLanguage


# -------------------------------------------------------------------------------------------------------------------#
class TB_VocabularyCollection:
	def __init__(self, conn, tableName="tb_Vocabulary"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_VocabularyRecord(row[0], row[1], row[2])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,Vocabulary,ID_Language)
			  VALUES(?,?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET Vocabulary={1}, ID_Language={2} WHERE ID = {3}""".format(self.tableName,
																						 record.vocabulary,
																						 record.idLanguage, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_VocabularyRecord(row[0], row[1], row[2])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################
class TB_VocabularyDenotationRecord:
	def __init__(self, id, idVocabulary, idVocabularyType, idLanguage, meaning):
		self.id = id
		self.idVocabulary = idVocabulary
		self.idVocabularyType = idVocabularyType
		self.idLanguage = idLanguage
		self.meaning = meaning

	def toTupel(self):
		return self.id, self.idVocabulary, self.idVocabularyType, self.idLanguage, self.meaning


# -------------------------------------------------------------------------------------------------------------------#
class TB_VocabularyDenotationCollection:
	def __init__(self, conn, tableName="tb_Vocabulary_Denotation"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_VocabularyDenotationRecord(row[0], row[1], row[2], row[3], row[4])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,ID_Vocabulary,ID_Vocabulary_Type,ID_Language,Meaning)
			  VALUES(?,?,?,?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET ID_Vocabulary={1},ID_Vocabulary_Type={2},ID_Language={3},Meaning={4} WHERE ID = {5}""".format(
			self.tableName, record.idVocabulary, record.idVocabularyType, record.idLanguage, record.meaning, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_VocabularyDenotationRecord(row[0], row[1], row[2], row[3], row[4])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid


####################################################################################################################
class TB_VocabularyDenotationTagRecord:
	def __init__(self, id, idVocabularyDenotation, idTag):
		self.id = id
		self.idVocabularyDenotation = idVocabularyDenotation
		self.idTag = idTag

	def toTupel(self):
		return self.id, self.idVocabularyDenotation, self.idTag


# -------------------------------------------------------------------------------------------------------------------#
class TB_VocabularyDenotationTagCollection:
	def __init__(self, conn, tableName="tb_Vocabulary_Denotation_Tag"):
		self.conn = conn
		self.tableName = tableName

	def getRecordByID(self, id):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE id={1}""".format(self.tableName, id)
		cur.execute(query)
		row = cur.fetchone()
		if row is not None:
			record = TB_VocabularyDenotationTagRecord(row[0], row[1], row[2])
			return record
		else:
			return None

	def insertRecord(self, record):
		sql = """INSERT INTO {0}(ID,ID_Vocabulary_Denotation,ID_Tag)
			  VALUES(?,?,?) """.format(self.tableName)
		cur = self.conn.cursor()
		cur.execute(sql, record.toTupel())
		return cur.lastrowid

	def removeRecordByID(self, record):
		sql = """DELETE FROM {0} WHERE ID ={1}""".format(self.tableName, record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def updateRecordByID(self, record):
		sql = """UPDATE {0} SET ID_Vocabulary_Denotation={1},ID_Tag={2} WHERE ID = {3}""".format(self.tableName,
																								 record.idVocabularyDenotation,
																								 record.idTag,
																								 record.id)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def insertCollection(self, collection):
		for record in collection:
			self.insertRecord(record)

	def removeCollection(self, collection):
		for record in collection:
			self.removeRecordByID(record)

	def updateCollection(self, collection):
		for record in collection:
			self.updateRecordByID(record)

	def getDataByCondition(self, condition="1=1"):
		cur = self.conn.cursor()
		query = """SELECT * FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur.execute(query)
		rows = cur.fetchall()
		records = []
		for row in rows:
			record = TB_VocabularyDenotationTagRecord(row[0], row[1], row[2])
			records.append(record)
		return records

	def updateDataByCondition(self, feld, condition):
		sql = """UPDATE {0} SET {1} WHERE {2}""".format(self.tableName, feld, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid

	def removeDataByCondition(self, condition):
		sql = """DELETE FROM {0} WHERE {1}""".format(self.tableName, condition)
		cur = self.conn.cursor()
		cur.execute(sql)
		return cur.lastrowid
