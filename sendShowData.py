import csv
from os import getenv
import sys

def searchSubstring(showData, showName):

    showInfo = []

    for row in showData:
        rowLower = row[1].lower()
        if showName == row[1] or showName.lower() == rowLower:
            showInfo.append(row)
    return showInfo


def getShowData(showName, seasons):
    fileHandler = open('showdata.csv', "r")
    showData = csv.reader(fileHandler,delimiter = ",") #  IMDb Data

    showInfo = []
    for row in showData: # Search for EXACT match 
        if showName == row[1] or showName.lower() == row[1].lower():
            showInfo.append(row)

    fileHandler.seek(1) # Return CSV to beginning
    trySubstringSearch = False

    if not showInfo: # If exact match could not be found...
        trySubstringSearch = True
        for row in showData: # try lowercase match
            rowLower = row[1].lower()
            if showName.lower() in rowLower:
                showInfo.append(row)

    fileHandler.seek(1)

    if trySubstringSearch:
        showInfo = searchSubstring(showInfo,showInfo[1][1]) # Search data once more with the best guess show name 

    showInfo = sorted(showInfo, key = lambda x: (int(x[2]), int(x[3]))) # Sort show based on season and episode
    print("Show Name: ")
    print(showInfo[1][1])
    
    seasons = showInfo[-1][2]
    bestEp = []

    for i in range(0,len(showInfo)):
        bestEp.append(float(showInfo[i][4])) # Pulling all episode ratings 

    bestEpRating = max(bestEp)
    worstEpRating = min(bestEp)

    index = bestEp.index(bestEpRating)
    lowestIndex = bestEp.index(worstEpRating)

    worstEpName = showInfo[lowestIndex][5]
    bestEpName = str(showInfo[index][5])

    cleanedList = []
    tempDict = {}

    for item in showInfo:
        seasonName = "Season " + item[2]
        if seasonName not in tempDict: # Checks to see if season is not in dictionary
            cleanedList.append(dict(tempDict)) # Adds previous season to dictionary
            tempDict.clear()
            tempDict[seasonName] = [] # Reinitialize tempDict
        if seasonName in tempDict:

            tempList = [item[5],item[4]] # Adds Episode name, Rating to list 
            print(item[5])
            tempDict[seasonName].append(tempList)
    cleanedList.append(dict(tempDict)) # Adds last season to dictionary

    dictToReturn = {}
    dictToReturn[showInfo[1][1]] = cleanedList
    print(dictToReturn)
    dictToReturn = {k: v for k, v in dictToReturn.items() if v is not None} # Deletes any empty values
    return dictToReturn , seasons, bestEpName, bestEpRating, worstEpName, worstEpRating



#Typically, a triple nested for loop is extremely ineffective at O(N^3). However, since we know that a given show won't have a extremely high amount of episodes this is okay. 
'''
for item in listFinal:
    for season,episodeList in item.items():
        print(season, ': ')
        for episode in episodeList:
            print("Episode:", episode[0], "Rating:", episode[1])
'''
