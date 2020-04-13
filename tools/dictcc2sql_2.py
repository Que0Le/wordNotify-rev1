import sqlite3
# from os import listdir
from os.path import isfile, join
import glob
import datetime

# con = sqlite3.connect(":memory:")
con = sqlite3.connect("../testdb_2.db")
con.execute(f"CREATE TABLE IF NOT EXISTS ALL_DICTS(id integer PRIMARY KEY AUTOINCREMENT, table_name text NOT NULL, size integer)")

def filebrowser(parents="", ext=""):
    "Returns files with an extension"
    return [f for f in glob.glob(f"{parents}*{ext}")]

x = filebrowser("../dicts/", ".txt")
print(x)

for file_path in x:
    print(f"working on {file_path}...")
    with open(file_path, "r", encoding='utf8') as f:
        table_name = f.readline().split(" ")[1].replace("-", "_")
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name}( \
            id integer PRIMARY KEY AUTOINCREMENT, \
            line text NOT NULL, \
            note text, \
            description text, \
            date_created timestamp, \
            last_modified timestamp \
            )")
        con.commit()
        print(f"created table {table_name}")
    querry = f"insert into {table_name}( \
        id, line, note, description, date_created, last_modified \
        ) values (?,?,?,?,?,?)"
    i = 1
    lines_arr = []
    with open(file_path, "r", encoding='utf8') as f:
        now = datetime.datetime.now()
        for line in f:
            # skip the comment lines, which starts with # @hoan
            if line.startswith("#") or len(line) == 0:
                continue
            lines_arr.append((None, line, "", "", now, now))
            if i%10000 == 0:
                con.executemany(querry, lines_arr)
                con.commit()
                lines_arr.clear()
                print(f"added {str(i)} lines")
                now = datetime.datetime.now()
            i+=1
        con.executemany(querry, lines_arr)
        con.commit()
        con.executemany("insert into ALL_DICTS(id, table_name, size) values (?,?,?)", [(None, table_name, i)])
        con.commit()


    