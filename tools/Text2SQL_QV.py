# -*- coding: utf-8 -*-
from DB_Dictionary_QV import DB_SqliteDictionary
from DB_Dictionary_QV import TB_VocabularyRecord
from DB_Dictionary_QV import TB_VocabularyCollection
from DB_Dictionary_QV import initTablesForDBDictionary
from DB_Dictionary import QueryExecuter

db_Dict = DB_SqliteDictionary("DB_Dictionary_QV.db")
conn = db_Dict.createConnection()


def escapeSpecialCharracter(str):
    return str.replace("'", "\'").replace('"', '\"').replace('%', '\%').replace('&', '\&').replace('#', '\#')


def lineTextAnalyzis(line):
    """

    :rtype: object
    """
    values = line.split("\t")
    if len(values) == 4:
        vocabulary = values[0]
        meaning = values[1]
        types = values[2]
        tags = values[3]
        return vocabulary, meaning, types, tags
    else:
        return None


def loadDataInDatabase(file_path, tableName):
    initTablesForDBDictionary(conn, tableName)
    with open(file_path, 'r', encoding="utf-8", errors="surrogateescape") as fp:
        tb_VocabularyColl = TB_VocabularyCollection(conn, tableName)
        lineIndex = 0
        skipIndex = 0
        for line in fp:
            lineIndex = lineIndex + 1
            print(lineIndex)
            # skip the comment lines, which starts with #
            if line.startswith("#") or len(line) == 0:
                skipIndex = skipIndex + 1
                continue
            tupelValues = lineTextAnalyzis(line)
            if tupelValues is None:
                skipIndex = skipIndex + 1
                continue
            vocabulary = tupelValues[0]
            meaning = tupelValues[1]
            types = tupelValues[2]
            tags = tupelValues[3]
            # insert meaning into the database with id key of the vocabulary'''
            n_Record = TB_VocabularyRecord(None, vocabulary, meaning, types, tags)
            tb_VocabularyColl.insertRecord(n_Record)

        conn.commit()
        conn.close()
        print("skipped Lines from {0} :{1}/{2}".format(file_path, skipIndex, lineIndex))


loadDataInDatabase("..\dicts\d-e.txt", "tb_Vocabulary_DE")
print("Bitte überprüfen")
