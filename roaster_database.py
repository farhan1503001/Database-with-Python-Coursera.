import json
import sqlite3
#Initiating the database
connection=sqlite3.connect(database='roaster_db.sqlite')
curr=connection.cursor()#Cursor initiated
#Creating tables for the database
# Do some setup
curr.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

#Now reading the json file
filename=open('roster_data.json')#File opened
raw_data=filename.read()#Reading the file
dataset=json.loads(raw_data)#Now loaded the json data it looks similar to simple dataset
for element in dataset:
    name=element[0]
    title=element[1]
    role=element[2]
    curr.execute('insert or ignore into User(name) values(?)',(name,))
    user_id=curr.execute('select id from User where name=?',(name,)).fetchone()[0]#Extracting user id
    curr.execute('insert or ignore into Course(title) values(?)',(title,))
    c_id=curr.execute('select id from Course where title=?',(title,)).fetchone()[0]
    curr.execute('insert or ignore into Member(user_id,course_id,role) values(?,?,?)',(user_id,c_id,role))
    connection.commit()

