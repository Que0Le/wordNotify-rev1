# -*- coding: utf-8 -*-
from DB_Dictionary import DB_SqliteDictionary
from DB_Dictionary import TB_LanguageRecord
from DB_Dictionary import TB_LanguageCollection
from DB_Dictionary import TB_VocabularyRecord
from DB_Dictionary import TB_VocabularyCollection
from DB_Dictionary import TB_VocabularyDenotationRecord
from DB_Dictionary import TB_VocabularyDenotationCollection
from DB_Dictionary import QueryExecuter

db_Dict = DB_SqliteDictionary("DB_Dictionary_V1.db")
conn = db_Dict.createConnection()
vocabularyColl = TB_VocabularyCollection(conn)
vocabularyDenotationColl = TB_VocabularyDenotationCollection(conn)


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
        f""" {TB_VocabularyRecord.ID_Language}={id_Language} AND {TB_VocabularyRecord.Vocabulary} LIKE  '{keyword}%' ORDER BY {TB_VocabularyRecord.Vocabulary}""")
    conn.commit()
    return jsonGenerator(records)


# print(getWordByKeyword(1, "Fuss"))

# GET URL: word/{id_Vocabulary}
# return Json Object
def getWorByID(id_Vocabulary):
    record = vocabularyColl.getRecordByID(id_Vocabulary)
    if record is None:
        return ""
    else:
        return record.toJson()


#print(getWorByID(100))


# GET URL: meaning/{id_Language}/{id_Vocabulary}
# return list of words suggested for keyword in Json format
def getWordMeaning(id_Language, id_Vocabulary):
    records = vocabularyDenotationColl.getDataByCondition(
        f""" {TB_VocabularyDenotationRecord.ID_Language}={id_Language} AND {TB_VocabularyDenotationRecord.ID_Vocabulary}={id_Vocabulary} ORDER BY {TB_VocabularyDenotationRecord.ID}""")
    conn.commit()
    return jsonGenerator(records)

# print(getWordMeaning(2, 44))
