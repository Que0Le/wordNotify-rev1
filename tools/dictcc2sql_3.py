import sqlite3
# from os import listdir
from os.path import isfile, join
import glob
import datetime
import re

# con = sqlite3.connect(":memory:")
con = sqlite3.connect("../testdb_3.db")
con.execute(f"CREATE TABLE IF NOT EXISTS ALL_DICTS(\
    w_id integer PRIMARY KEY AUTOINCREMENT,\
    table_name text NOT NULL,\
    size integer)")

def filebrowser(parents="", ext=""):
    "Returns files with an extension"
    return [f for f in glob.glob(f"{parents}*{ext}")]

def lineTextAnalyzis(line):
    values = line.split("\t")
    if len(values) == 4:
        vocabulary = values[0]
        meaning = values[1]
        types = values[2]
        tags = values[3]
        return vocabulary, meaning, types, tags
    else:
        return None

x = filebrowser("../dicts/", ".txt")
print(x)

for file_path in x:
    print(f"working on {file_path}...")
    with open(file_path, "r", encoding='utf8') as f:
        table_name = f.readline().split(" ")[1].replace("-", "_")
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name}( \
            w_id INTEGER PRIMARY KEY AUTOINCREMENT, \
            word TEXT NOT NULL,\
            gender TEXT,\
            w_types TEXT,\
            features TEXT, \
            also_form TEXT,\
            long_form TEXT,\
            plural TEXT,\
            past_form TEXT,\
            pronunciation TEXT,\
            meaning TEXT,\
            tags TEXT,\
            antonyms TEXT,\
            synonyms TEXT,\
            raw TEXT, \
            note TEXT, \
            description TEXT, \
            date_created timestamp, \
            last_modified timestamp \
            )")
        con.commit()
        print(f"created table {table_name}")
    querry = f"insert into {table_name}\
        (w_id, word, gender, w_types, features, also_form, long_form, plural, \
        past_form, pronunciation, meaning, tags, antonyms, synonyms, \
        raw, note, description, date_created, last_modified) \
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    i = 1
    lines_arr = []
    with open(file_path, "r", encoding='utf8') as f:
        date_created = datetime.datetime.now()
        for line in f:
            # skip the comment lines, which starts with # @hoan
            if line.startswith("#") or len(line) == 0:
                continue
            ### processing
            values = line.split("\t")
            if len(values) != 4:
                continue
            w_id, word, gender, w_types, features, also_form, long_form, plural, \
            past_form, pronunciation, meaning, tags, antonyms, synonyms, \
            raw, note, description, last_modified = \
                None, "", "","", "", "", "","", "", "", "","", "", "", "","", "", ""
            meaning = values[1].strip()
            w_types = values[2].strip().replace(" ", ",")
            tags = values[3].strip().replace(" ", ",")
            # Extract gender
            if values[2] == "noun":
                gender_temp = re.findall("{\w}", values[0])
                if len(gender_temp) > 0:
                    gender = '|'.join(gender_temp)  # '{f}|{n}'
            # Extract 'features'
            features_temp = re.findall("\[.*?\]", values[0])
            if len(features_temp) > 0:
                features = '|'.join(features_temp)  # '[ugs.]|[ausgelassen feiern]'
            # Clean up word
            word = re.sub(r"{\w+}|\[.*?\]", "", values[0]).strip()

            lines_arr.append((w_id, word, gender, w_types, features, also_form, long_form, plural, \
                past_form, pronunciation, meaning, tags, antonyms, synonyms, \
                raw, note, description, date_created, last_modified))
            if i%10000 == 0:
                con.executemany(querry, lines_arr)
                con.commit()
                lines_arr.clear()
                print(f"added {str(i)} lines")
                date_created = datetime.datetime.now()
            i+=1
        con.executemany(querry, lines_arr)  # last iterator i%10000
        con.commit()
        con.executemany("insert into ALL_DICTS(id, table_name, size) values (?,?,?)", [(None, table_name, i)])
        con.commit()
    break


    