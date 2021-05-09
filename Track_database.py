import xml.etree.ElementTree as etree
import sqlite3
#Initiating the database
connection= sqlite3.connect(database='itunes.sqlite')
#Defining the cursor to the dataset
curr=connection.cursor()
#Creating tables in the dataset
curr.executescript(
'''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);'''
)
#Now opening the database file
filename=open('Library.xml')
#Now finding the expected data and setting them in a variable 
temp_data=etree.parse(filename)
entire_data=temp_data.findall(path='dict/dict/dict')
print("Dict Count ",len(entire_data))
#Now defining a function for searching inside xml elemenet tree
#First we will match tag <>and inside key text if they are the coloumn we want then set found true
#next element will be the data whose value we want so return the text and break
def look(d,key):
    flag=False
    for leaf in d:
        if flag==True: 
            return leaf.text
        if leaf.tag=='key' and leaf.text==key:
            flag=True
        
    return None
#Traverse through entire tree go to every dictionary inside that and for them find values using function
for entry in entire_data:
    if (look(entry,'Track ID') is None):
        continue
    
    name = look(entry, 'Name')#Find the name value of the entry 
    artist = look(entry, 'Artist')#Find the artist value of entry
    album = look(entry, 'Album')#Find the Album value of entry
    count = look(entry, 'Play Count')#Find the count value of entry
    rating = look(entry, 'Rating')#Find the rating value of entry
    genre=look(entry,'Genre')
    length = look(entry, 'Total Time')#Find the length value of entry

    if (name is None ) or (artist is None) or (album is None) or (genre is None): #If there is no name then next operation will not be performed
        continue
    curr.execute('insert or ignore into Artist(name) values(?)',(artist,))
    artist_id=curr.execute('select id from Artist where name=?',(artist,)).fetchone()[0]
    curr.execute('insert or ignore into Album(artist_id,title) values(?,?)',(artist_id,album))
    album_id=curr.execute('select id from Album where title=?',(album,)).fetchone()[0]
    curr.execute('insert or ignore into Genre(name) values(?)',(genre,))
    genre_id=curr.execute('select id from Genre where name=?',(genre,)).fetchone()[0]
    curr.execute('insert or ignore into Track(title,album_id,genre_id,len,rating,count) values(?,?,?,?,?,?)',(name,album_id,genre_id,length,rating,count))
    
    #Commit the cursor
    connection.commit()

