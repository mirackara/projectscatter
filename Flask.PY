from flask import Flask, request, url_for, redirect, render_template
from GenerateShowData import *
import random
from bs4 import BeautifulSoup
import requests





Show = GetShowData('3107288')
ShowDataPoint = Show.listSeriesData()

def getStats(DataPoint):
    lastEp = DataPoint[-1][0]
    Y = []
    #Gets all Y's into a list
    for i in range (0,lastEp):
        Y.append(DataPoint[i][1])
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




@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)

    ##Scrape Data from IMDB.com

    # Create an instance of the IMDb class
    tvShow = IMDb()
    showID = tvShow.search_movie(processed_text)
    del showID[1:]
    showID = str(showID)
    showID = showID[11:]
    showID = int(showID.split("[")[0])
    print('Show ID:')
    print(showID)
    Show = GetShowData(showID)
    DataPoint = Show.listSeriesData()
    ScaledYAxis, lastEp = getStats(DataPoint)

    template = render_template('index.html',series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = DataPoint)
    return template




if __name__ == '__main__':
    app.run()

