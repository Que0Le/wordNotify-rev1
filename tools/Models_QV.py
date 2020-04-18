# -*- coding: utf-8 -*-
from DB_Dictionary_QV import DB_SqliteDictionary
from DB_Dictionary_QV import TB_VocabularyRecord
from DB_Dictionary_QV import TB_VocabularyCollection
from DB_Dictionary import QueryExecuter

db_Dict = DB_SqliteDictionary("DB_Dictionary_QV.db")
conn = db_Dict.createConnection()
vocabularyColl = TB_VocabularyCollection(conn, "tb_Vocabulary_DE")


###############################################################################################################
# !!!Warning: SQL-INJECTION
# implement tasks for model layer
# HelperFunction
def jsonGenerator(records):
    strJson = ""
    for record in records:
        strJson = strJson + "," + record.toJson()
    if len(strJson) > 0:
        strJson = strJson[1:len(strJson)]
    return "[" + strJson + "]"


# REST API:
# GET URL: word/{id_Language/{keyword}
# return list of words suggested for keyword in Json format


def getWordByKeyword(id_Language, keyword):
    records = vocabularyColl.getDataByCondition(
        f""" {TB_VocabularyRecord.Vocabulary} LIKE  '{keyword}%' ORDER BY {TB_VocabularyRecord.Vocabulary}""")
    conn.commit()
    return jsonGenerator(records)


# print(getWordByKeyword(1, "Fuss"))
# print(getWordByKeyword(1, "Fuss"))
# GET URL: word/{id_Vocabulary}
# return Json Object


def getWordByID(id_Vocabulary):
    record = vocabularyColl.getRecordByID(id_Vocabulary)
    if record is None:
        return ""
    else:
        return record.toJson()


def getAllMeaningsOfWordbyID(id_Vocabulary):
    record = vocabularyColl.getRecordByID(id_Vocabulary)
    if record is None:
        return ""
    else:
        records = vocabularyColl.getDataByCondition(
            f""" {TB_VocabularyRecord.Vocabulary} LIKE  '{record.vocabulary}' ORDER BY {TB_VocabularyRecord.Meaning}""")
    conn.commit()
    return jsonGenerator(records)


print(getAllMeaningsOfWordbyID(210))
