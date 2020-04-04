import sqlite3
# from os import listdir
from os.path import isfile, join
import glob
persons = [
    ("Hugo", "Boss"),
    ("Calvin", "Klein")
]

# con = sqlite3.connect(":memory:")
con = sqlite3.connect("testdb.db")

# Create the table
# con.execute("""CREATE TABLE IF NOT EXISTS projects (id integer PRIMARY KEY AUTOINCREMENT, line text NOT NULL)""")

# Fill the table
# con.executemany("insert into person(firstname, lastname) values (?,?)", persons)

# onlyfiles = [f for f in listdir("dicts") if isfile(join("dicts", f))]
# print(onlyfiles)

def filebrowser(parents="", ext=""):
    "Returns files with an extension"
    return [f for f in glob.glob(f"{parents}*{ext}")]

x = filebrowser("dicts/", ".txt")
print(x)

for file_path in x:
    print(f"working on {file_path}...")
    with open(file_path, "r", encoding='utf8') as f:
        table_name = f.readline().split(" ")[1].replace("-", "_")
        con.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(id integer PRIMARY KEY AUTOINCREMENT, line text NOT NULL)""")
        print(f"created table {table_name}")
    querry = f"insert into {table_name}(id, line) values (?,?)"
    i = 1
    lines_arr = []
    with open(file_path, "r", encoding='utf8') as f:
        # print(f.readline())
        for line in f:
            # print(line)
            lines_arr.append((None, line))
            if i%10000 == 0:
                con.executemany(querry, lines_arr)
                con.commit()
                lines_arr.clear()
                print(f"added {str(i)} lines")
            i+=1
        con.executemany(querry, lines_arr)
        con.commit()

    