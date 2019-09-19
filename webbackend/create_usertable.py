import sqlite3

dbname = 'appdata.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE userlist (\
  userID integer primary key AUTOINCREMENT,\
  name text,\
  rating real,\
  nationality text,\
  photo text\
)')

cur.execute('CREATE TABLE requestlist (\
  userID integer primary key,\
  latitude real,\
  longitude real\
)')

cur.execute('CREATE TABLE helpinglist (\
  TaskID integer primary key AUTOINCREMENT,\
  helperID int,\
  helpeeID int\
)')

conn.commit()
conn.close()