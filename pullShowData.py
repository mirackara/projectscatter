from configparser import ConfigParser

import mysql.connector


def cleanDictionary(show, showInfo):
    # total seasons
    bestEp = []
    for i in range(0, len(showInfo)):
        bestEp.append(float(showInfo[i][3]))  # Pulling all episode ratings
    bestEpRating = max(bestEp)
    worstEpRating = min(bestEp)

    index = bestEp.index(bestEpRating)
    lowestIndex = bestEp.index(worstEpRating)

    worstEpName = showInfo[lowestIndex][2]
    bestEpName = str(showInfo[index][2])

    cleanedList = []
    tempDict = {}
    showInfo.sort()
    totalSeasons = showInfo[-1][0]

    for item in showInfo:
        seasonName = "Season " + str(item[0])
        if seasonName not in tempDict:  # Checks to see if season is not in dictionary
            # Adds previous season to dictionary
            cleanedList.append(dict(tempDict))
            tempDict.clear()
            tempDict[seasonName] = []  # Reinitialize tempDict
        if seasonName in tempDict:
            epName = item[2][1:].replace("'", "")
            epName = epName.replace("\"", "")
            tempList = [epName, item[3]]  # Adds Episode name, Rating to list
            tempDict[seasonName].append(tempList)
    cleanedList.append(dict(tempDict))  # Adds last season to dictionary

    dictToReturn = {show: cleanedList}
    return dictToReturn, totalSeasons, bestEpName, bestEpRating, worstEpName, worstEpRating, show


def SQLRequest(name):
    # SQL Connection String
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
    mycursor.execute("SELECT * from tvShowsSQLDB WHERE parentTconst = %s ", (name,))
    result = mycursor.fetchall()

    # Partial Substring Search
    if len(result) == 0:
        print("No results! Attempting Partial Search...")
        mycursor.execute("SELECT * from tvShowsSQLDB WHERE parentTconst LIKE %s ", ('%' + name + '%',))
        result = mycursor.fetchall()

    currShow = ""
    showNames = []
    showInfo = {}
    for i in range(0, len(result)):
        if i == 0:
            currShow = result[0][1]
            showNames.append(currShow)
            showInfo[currShow] = [[result[0][2], result[0][3], result[0][5], result[0][4]]]
            continue
        if currShow != result[i][1]:
            currShow = result[i][1]
            showNames.append(currShow)
            showInfo[currShow] = [result[i][2], result[i][3], result[i][5], result[i][4]]
        showInfo[currShow].append([result[i][2], result[i][3], result[i][5], result[i][4]])

    # More than 1 show found
    if len(showNames) > 1:
        print(len(showNames), " shows found.")
        cnx.close()
        print("First Show: ", showNames)
        return -1000, 0, 0, 0, 0, 0, showNames

    # Just 1 show found
    elif len(showNames) == 1:
        show = showNames[0]
        print("Returning Show ", show)
        cnx.close()
        return cleanDictionary(show, showInfo[show])

    if len(showNames) == 0:
        print("No Show Found. Search Again")
        cnx.close()
        return -999, 0, 0, 0, 0, 0, 0
