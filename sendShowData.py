import csv
from os import getenv
import sys

def searchSubstring(showName):
    showData = csv.reader(open('dataFullSorted.csv', "r"),delimiter = ",") #  IMDb Data

    showInfo = []
    alreadyFound = False
    for row in showData:
        rowLower = row[1].lower()
        if showName == row[1] or showName.lower() == rowLower:
            showInfo.append(row)
    return showInfo


def getShowData(showName, seasons):
    showData = csv.reader(open('dataFullSorted.csv', "r"),delimiter = ",") #  IMDb Data

    showInfo = []
    alreadyFound = False
    for row in showData:
        rowLower = row[1].lower()
        if showName == row[1] or showName.lower() == rowLower:
            showInfo.append(row)

    showData = csv.reader(open('dataFullSorted.csv', "r"),delimiter = ",") #  IMDb Data
    trySubstringSearch = False

    if not showInfo:
        trySubstringSearch = True
        print("ShowInfo Empty!")
        for row in showData:
            rowLower = row[1].lower()
            if showName.lower() in rowLower:
                showInfo.append(row)

    if (trySubstringSearch):
        showInfo = searchSubstring(showInfo[1][1])

    showInfo = sorted(showInfo, key = lambda x: (int(x[2]), int(x[3]))) # Sort show based on season and episode
    print("Show Name: ")
    print(showInfo[1][1])
    print("Seasons: ")
    seasons = showInfo[-1][2]
    print(showInfo[-1][2])
    print("Episodes: ")
    bestEp = []
    for i in range(0,len(showInfo)):
        bestEp.append(float(showInfo[i][4]))
    highestRating = max(bestEp)
    lowestRating = min(bestEp)
    index = bestEp.index(highestRating)
    lowestIndex = bestEp.index(lowestRating)
    print("Best episode: ")
    print(showInfo[index][5])
    print("Worst Episode: ")
    print(showInfo[lowestIndex][5])
    worstEpName = showInfo[lowestIndex][5]
    bestEpName = str(showInfo[index][5])
    bestEpRating = highestRating
    worstEpRating = lowestRating
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
            tempDict[seasonName].append(tempList)
    cleanedList.append(dict(tempDict)) # Adds last season to dictionary

    dictToReturn = {}
    dictToReturn[showInfo[1][1]] = cleanedList
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
## Format neeeded:
## data : [{name: "Season X", dataPoints: [{label: "Ep. X"}, y: ratingNum]}]