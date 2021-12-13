from copy import deepcopy

from django.shortcuts import render
from django.http import HttpResponse
from sendShowData import *
import json


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
            seasons = 0
            currShowData, seasons = getShowData(show, seasons, True)
            showData.append(deepcopy(currShowData))
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'true',
                'showList': json.dumps(listOfShows)}
    except:
        print("Error!")
        return {'test': json.dumps(showData), 'numOfShows': len(listOfShows), 'lastShowAdded': 'false',
                'showList': json.dumps(listOfShows[:1])}


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
        testSend = request.POST.get('toSend')
        print('toSend: ' , testSend)
        print(request.POST)
        searchedShow = request.POST['searchBar']
        print(searchedShow)
        listOfShows = searchedShow.split(",")
        print("Compare : ", listOfShows)
        return render(request, "multigraph.html", getMultipleShows(listOfShows))


def handleSearch(request):
    print("ok")
    searchReq = request.POST['searchBar']
    print(searchReq)
