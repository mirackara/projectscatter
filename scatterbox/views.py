from copy import deepcopy

from django.shortcuts import render, redirect
from django.http import HttpResponse
from sendShowData import *
import json

currShows = []


def get(showName):
    seasons = 0
    bestEpName = ""
    worstEpName = ""
    bestEpRating = 0.0
    worstEpRating = 0.0
    returnedName = ""
    showData, seasons, bestEpName, bestEpRating, worstEpName, worstEpRating, returnedName = getShowData(
        showName, seasons, False)
    statusCode = 200
    headers = {'Content-Type': 'text/html'}
    return {'showName': returnedName, 'seasons': seasons, 'showData': json.dumps(showData), 'bestEpName': bestEpName,
            'bestEpRating': bestEpRating,
            'worstEpName': worstEpName, 'worstEpRating': worstEpRating, 'statusCode': statusCode}


def getMultipleShows(listOfShows):
    showData = []
    try:
        for show in listOfShows:
            print("Curr Show: ", show)
            seasons = 0
            currShowData, seasons = getShowData(show, seasons, True)
            showData.append(deepcopy(currShowData))
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'true',
                'showList': json.dumps(listOfShows)}
    except:
        print("Error!")
        print("showData ERROR : ", showData)
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'false',
                'showList': json.dumps(listOfShows[:1])}


def indexHandler(request):
    return redirect('/search/')


# Request Handler
def eventHandler(request):
    # Home Screen
    if request.POST == {}:
        print(request.POST)
        return render(request, "home.html", get("Breaking Bad"))
    # Search
    elif 'searchBtn' in request.POST:
        print(request.POST)
        searchedShow = request.POST['searchBar']
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
        currShows.append(searchedShow)
        return render(request, "multigraph.html", getMultipleShows(currShows))
