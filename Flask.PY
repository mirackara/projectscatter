from flask import Flask, request, url_for, redirect, render_template
from GenerateShowData import *
import random
from bs4 import BeautifulSoup
import requests





Show = GetShowData('3107288')
ShowDataPoint = Show.listSeriesData()

def getStats(ShowDataPoint):
    lastEp = ShowDataPoint[-1][0]
    Y = []
    #Gets all Y's into a list
    for i in range (0,lastEp):
        Y.append(ShowDataPoint[i][1])
        averageYRating = sum(Y) / len(Y)
        averageYRating = round(averageYRating,2)
        ScaledYAxis = averageYRating - 3
        ScaledYAxis = round(ScaledYAxis, 2)
    return ScaledYAxis, lastEp

ScaledYAxis, lastEp = getStats(ShowDataPoint)

 

app = Flask(__name__)
@app.route('/')
def index():
    template = render_template('index.html',series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = ShowDataPoint)
    return template




@app.route('/', methods=["GET", "POST"])
def my_form_post():
    searchText = request.form['text']

    print(searchText)
    if (searchText ==''):
        Show = GetShowData('3107288')
        ShowDataPoint = Show.listSeriesData()
        getStats(ShowDataPoint)
        ScaledYAxis, lastEp = getStats(ShowDataPoint)

        template = render_template('index.html',series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = ShowDataPoint)
        return template

    
    # Create an instance of the IMDb class
    tvShow = IMDb()
    showID = tvShow.search_movie(searchText)
    del showID[1:]
    showID = str(showID)
    showID = showID[11:]
    showID = int(showID.split("[")[0])
    print('Show ID:')
    print(showID)
    Show = GetShowData(showID)
    DataPoint = Show.listSeriesData()
    ScaledYAxis, lastEp = getStats(DataPoint)

    template = render_template('index.html',processed_text = searchText, series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = DataPoint)
    return template , searchText


if __name__ == '__main__':
    app.run()

