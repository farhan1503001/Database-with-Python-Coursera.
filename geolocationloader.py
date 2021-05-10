#Here our programm loads the name of the univerisities from where.data and 
import urllib.request,urllib.parse,urllib.error
import http
import json
import sqlite3
import time
import sys
import ssl

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
#Here A
if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"
#Initiating the database connection
connection=sqlite3.connect('geography.sqlite')
curr=connection.cursor()#Initiating the cursor.
#Creating the main table
curr.execute('create table if not exists location(address text, geodata text)')
#For ignoring ssl certificate errors we set parameters
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE
#Now we will open the file
data=open('where.data')
count=0
for line in data:
    #First we will check if the value is in the database if yes then we will print it
    address=line.strip()
    print("")
    curr.execute('select geodata from location where address=?',(memoryview(address.encode()),))
    #Now checking the presence of value
    try:
        data= curr.fetchone()[0]
        print("Data Found ",data)
        continue
    except:
        pass
    #Now we will move for the condition when the value is not present in the database so we are to insert it
    params=dict()
    params['address']=address
    if api_key is not False:
        params['key']=api_key
    #print(params)
    #Creating the search url with our address
    parse_url=urllib.parse.urlencode(params)
    url=serviceurl+parse_url
    #Now we will perform data retrivation from the url 
    request_url=urllib.request.urlopen(url,context=ctx)#Opened the url in back like browser
    data=request_url.read().decode()
    count=count+1
    #print("Encoded Url ",parse_url)
    #print(data)#Now seeing the retrived data
    #Now converting the data to it's json format to check some parameter it's optional & may not need always as
    #the data is already in json format
    try:
        js=json.loads(data)
    except:
        print(data)
        continue #If the data is present no need to insert it which we will perform next
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break
    #Otherwise insert the data into the table
    curr.execute('insert or ignore into location(address,geodata) values(?,?)',(memoryview(address.encode()),memoryview(data.encode())))
    connection.commit()

    if count%10==0:
        print('Taking pause for 5 s while retrieving')
        time.sleep(5)

    



