import json
from copy import deepcopy

from django.shortcuts import render, redirect

from pullShowData import *

currShows = []
def get(showName):
    seasons = 0
    bestEpName = ""
    worstEpName = ""
    bestEpRating = 0.0
    worstEpRating = 0.0
    returnedName = ""
    showData, seasons, bestEpName, bestEpRating, worstEpName, worstEpRating, returnedName = SQLRequest(
        showName)
    # Multiple Shows Found
    if showData == -1000:
        for i in range(0, len(returnedName)):
            returnedName[i] = returnedName[i].replace("'", '')
            print(returnedName[i])
        headers = {'Content-Type': 'text/html'}
        return {'showName': json.dumps(returnedName), 'seasons': seasons, 'showData': json.dumps(showData),
                'bestEpName': bestEpName,
                'bestEpRating': bestEpRating,
                'worstEpName': worstEpName, 'worstEpRating': worstEpRating, 'statusCode': 401}

    # No Show Found
    if showData == -999:
        print("Unable to Load show.")
        showData, seasons, bestEpName, bestEpRating, worstEpName, \
        worstEpRating, returnedName = SQLRequest("How I met your mother")
        statusCode = 404
        headers = {'Content-Type': 'text/html'}
        return {'showName': json.dumps(returnedName), 'seasons': seasons, 'showData': json.dumps(showData),
                'bestEpName': bestEpName,
                'bestEpRating': bestEpRating,
                'worstEpName': worstEpName, 'worstEpRating': worstEpRating, 'statusCode': statusCode}

    print("Show Data: ", showData)
    print("Seasons: ", seasons)
    statusCode = 200
    headers = {'Content-Type': 'text/html'}
    return {'showName': json.dumps(returnedName), 'seasons': seasons, 'showData': json.dumps(showData),
            'bestEpName': bestEpName,
            'bestEpRating': bestEpRating,
            'worstEpName': worstEpName, 'worstEpRating': worstEpRating, 'statusCode': statusCode}


def getMultipleShows(listOfShows):
    showData = []
    try:
        for show in listOfShows:
            print("Curr Show: ", show)
            seasons = 0
            statusCode = 0
            currShowData, seasons, bestEpName, bestEpRating, worstEpName, \
            worstEpRating, returnedName = SQLRequest(show)
            # Multiple Shows Found
            if currShowData == -1000:
                print("-1000 Error Code")
                for i in range(0, len(returnedName)):
                    returnedName[i] = returnedName[i].replace("'", '')
                returnedName.append(show)
                headers = {'Content-Type': 'text/html'}
                return {'showName': json.dumps(returnedName), 'seasons': seasons, 'test': json.dumps(showData),
                        'numOfShows': len(listOfShows), 'lastShowAdded': 'false', 'showList': json.dumps(listOfShows),
                        'statusCode': 401}
            else:
                showData.append(deepcopy(currShowData))
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'true',
                'showList': json.dumps(listOfShows), 'statusCode': 200, 'showName': '200'}
    except KeyError:
        print("Error!", KeyError)
        print("showData ERROR : ", showData)
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'false',
                'showList': json.dumps(listOfShows[:1]), 'statusCode': 404, 'showName': '404'}

def indexHandler(request):
    return redirect('/search/')

# Request Handler
def eventHandler(request):
    # Home Screen
    if request.POST == {}:
        print(request.POST)
        return render(request, "home.html", get("How I met your mother"))
    # Search
    elif 'searchBtn' in request.POST:
        print(request.POST)
        searchedShow = request.POST['searchBar']
        if len(searchedShow) < 3:
            returningParams = get("How I Met your Mother")
            returningParams['statusCode'] = 400
            return render(request, "home.html", returningParams)

        return render(request, "home.html", get(searchedShow))
    # Compare
    elif 'compareBtn' in request.POST:
        searchedShow = request.POST['searchBar']
        searchedShowStr = request.POST['showsToCompare']
        searchedShowList = searchedShowStr.split(",")
        for show in searchedShowList:
            currShows.append(show)
        return redirect('/compare/')


def handleSearch(request):
    print("ok")
    searchReq = request.POST['searchBar']
    print(searchReq)


def compareHandler(request):
    print("In Request: ", request.POST)
    # Initial Load
    if request.POST == {}:
        print("CompareHandler")
        print(request.POST)
        print(currShows)
        return render(request, "multigraph.html", getMultipleShows(currShows))
    # Clear All
    elif 'clearMe' in request.POST:
        print("Removing all!")
        currShows.clear()
        return redirect('/search/')
    # Add Show
    elif 'compareBtn' in request.POST:
        searchedShow = request.POST['searchBar']
        showsToRemoveList = request.POST['showsToRemove'].split(",")
        # Remove show from list if show is cleared on form
        for show in showsToRemoveList:
            if show in currShows:
                currShows.remove(show)
        if len(searchedShow) < 3:
            requestParams = getMultipleShows(currShows)
            requestParams['lastShowAdded'] = 'false'
            requestParams['statusCode'] = 400
            return render(request, "multigraph.html", requestParams)

        currShows.append(searchedShow)

        return render(request, "multigraph.html", getMultipleShows(currShows))
