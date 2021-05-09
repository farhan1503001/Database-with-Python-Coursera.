import sqlite3
#Importing the database
connector=sqlite3.connect('email_db.sqlite')
#Initiating the cursor
curr=connector.cursor()
#Drop table if count exists
curr.execute('DROP TABLE IF EXISTS Counts')
#Now create table count
curr.execute('create table Counts (org TEXT, count INTEGER)')
#now open our file
filename=open(file='mbox.txt')
i=0
for line in filename:
    if not line.startswith('From: '): continue
    pieces=line.split()
    org=pieces[1].split(sep='@')[-1]
    #org=temp[-2]+temp[-1]
    curr.execute('select * from Counts where org =?',(org,))
    row=curr.fetchone()
    if row is None:
        curr.execute('Insert into Counts(org,count) values (?,1)',(org,))
    else:
        curr.execute('Update Counts set count=count+1 where org=?',(org,))

    connector.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in curr.execute(sqlstr):
    print(str(row[0]), row[1])

curr.close()

