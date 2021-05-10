import sqlite3
import json
import codecs

conn = sqlite3.connect('geography.sqlite')#Initiating database
curr = conn.cursor()#Initiating the cursor of the database

curr.execute('SELECT * FROM Location')
filename = codecs.open('geo.js', 'w', "utf-8")
filename.write("myData = [\n")
count = 0
for row in curr :
    data = str(row[1].decode())
    try: 
        js = json.loads(str(data))#Loading the dataset in json format 
    except: 
        continue#If the data is not json readible then ignore next operations

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]#Latitude is in results-0-geometry dict-location_dict-lat
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    address = js['results'][0]['formatted_address']
    address = address.replace("'", "")
    try :
        print(address, lat, lng)

        count = count + 1
        if count > 1 : filename.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        filename.write(output)
    except:
        continue

filename.write("\n];\n")
curr.close()
filename.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")


