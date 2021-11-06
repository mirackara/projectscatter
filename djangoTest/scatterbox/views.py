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


# Create your views here.
# Request Handler
def testHandler(request):
    print(request.POST)
    if request.POST == {}:
        print(request.POST)
        return render(request, "home.html", get("Breaking Bad"))
    elif 'searchBtn' in request.POST:
        print(request.POST)
        searchedShow = request.POST['searchBar']
        return render(request, "home.html", get(searchedShow))
    elif 'compareBtn' in request.POST:
        searchedShow = request.POST['searchBar']
        print(request.POST)
        return render(request, "home.html", get(searchedShow))


def handleSearch(request):
    print("ok")
    searchReq = request.POST['searchBar']
    print(searchReq)
