import sqlite3

connection = sqlite3.connect('data_base.db')
cur = connection.cursor()
cur.execute('drop table if exists base')
TABLE = """create table base (
                           id integer primary key autoincrement,
                           start_time DATETIME not null,
                           end_time DATETIME not null
                           );
                           """

cur.execute(TABLE)
connection.close()