import csv
from configparser import ConfigParser

import mysql.connector

appConfig = ConfigParser()
appConfig.read("App.ini")
host = appConfig.get("CoreContext", "host")
user = appConfig.get("CoreContext", "user")
password = appConfig.get("CoreContext", "password")
database = appConfig.get("CoreContext", "database")
port = appConfig.get("CoreContext", "port")

cnx = mysql.connector.connect(user=user, password=password,
                              host=host, port=port,
                              database=database,
                              ssl_disabled=False)
mycursor = cnx.cursor()
print("Uploading to SQL DB..")
entryNum = 0
multi = 0
percentageDone = 0.00
with open('showdata.csv') as csvfile:
    showlistRaw = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in showlistRaw:
        if row[0] == "tconst":
            continue
        query = 'INSERT INTO tvShowsSQLDB (tconst, parentTConst, seasonNumber, episodeNumber, averageRating,epName) values(\'%s\', \'%s\', %s, %s, %s,\' %s\')' % (
            row[0], row[1], row[2], row[3], row[4], row[5])
        try:
            mycursor.execute(query)
            entryNum += 1
            # Upon the 1000th row, we commit to the SQL Server
            if entryNum == 1000:
                multi += 1
                entryNum = 0
                print("Last Entry: ", row[0])
                print(multi, "K enteries Uploaded")
                cnx.commit()
        except KeyError:
            print("Error, Unable to add value ", row)
            continue
cnx.commit()
print(mycursor.rowcount, "record inserted.")
