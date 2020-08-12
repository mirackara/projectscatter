from flask import Flask, request, url_for, redirect, render_template
from GenerateShowData import *
import random
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re
import ast 
import urllib.request
import os
import base64



def getStats(ShowDataPoint):
    try:
        lastEp = ShowDataPoint[-1][0]
        Y = []
        #Gets all Y's into a list
        for i in range (0,lastEp):
            Y.append(ShowDataPoint[i][1])
            averageYRating = sum(Y) / len(Y)
            averageYRating = round(averageYRating,2)
            ScaledYAxis = averageYRating - 3
            ScaledYAxis = round(ScaledYAxis, 2)
    except:
        return ScaledYAxis, lastEp
    return ScaledYAxis, lastEp


##Graphs The Flash show data as starting graph
Show = GetShowData('3107288')
ShowDataPoint = Show.listSeriesData()
ScaledYAxis, lastEp = getStats(ShowDataPoint)

def searchSite():
        #If user searches for an empty field, the page will default to grabbing The Flash data
        showPoster = os.path.join(app.config['UPLOAD_FOLDER'], 'showPoster3107288.jpg')
        template = render_template('index.html',series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = ShowDataPoint,showPoster = showPoster)
        return template


def searchShow(searchText):
    tvShow = IMDb()
    #In order to speed up the graphing process drastically, we can store graph data in a local CSV instead of calling IMDb().
    df = pd.read_csv('TopShowData.csv' ,quoting=csv.QUOTE_ALL)

    #Raw Data parsed from IMDB's website search needs to have show ID stripped
    showIDNum = tvShow.search_movie(searchText)
    del showIDNum[1:]
    showIDNum = str(showIDNum)
    showIDNum = showIDNum[11:]
    showIDNum = int(showIDNum.split("[")[0])
    ShowPoster = GetShowData(str(showIDNum))

    #Clone showID 
    showID = showIDNum
    print('Show ID:')
    print(showIDNum)
    Show = GetShowData(showIDNum)
    def rowIndex(row):
        return row.name

        
    if df['ShowID'].str.contains(str(showID)).any():
        print ("Show Exists!")
        dfChosen = df[df["ShowID"].str.contains(str(showID))]
        showName = list(dfChosen["ShowName"])
        index = dfChosen.apply(rowIndex, axis=1)
        showNum = list(index)[0]
        showID = list(dfChosen["ShowID"])
        lastEp = list(dfChosen["LastEp"])
        ScaledYAxis = 7.6
        print(dfChosen)
        showData = dfChosen.loc[showNum][-1]

        showData = str(showData)
        showName = str(showName[0])
        showID = showID[0]
        lastEp = int(lastEp[0])
        showData = ast.literal_eval(showData) 
        # ShowPoster.getPoster()

        # showPoster = os.path.join(app.config['UPLOAD_FOLDER'], 'showPoster'+str(showIDNum)+'.jpg')

        template = render_template('index.html',processed_text = searchText, series = showName,finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = showData)
        return template , searchText
    else:
        print('Need to add!')
            
        # Create an instance of the IMDb class
        print('Show ID:')
        print(showIDNum)
        Show = GetShowData(showIDNum)
        GetShowData(showIDNum).getPoster()
        DataPoint = Show.listSeriesData()
        ScaledYAxis, lastEp = getStats(DataPoint)
        strData = str(DataPoint)
        df = pd.read_csv('TopShowData.csv' ,quoting=csv.QUOTE_ALL)
        print('Show Does Not Exist In DataBase!')
        df.loc[-1] = ["'" + str(showID) + "'" , Show.getName() , str(lastEp) ,  strData]  # adding a row
        df.index = df.index + 1  # shifting index
        df = df.sort_index() 
        df.to_csv('TopShowData.csv' , index=False)
        showPoster = os.path.join(app.config['UPLOAD_FOLDER'], 'showPoster'+str(showIDNum)+'.jpg')
        
        template = render_template('index.html',processed_text = searchText, series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = DataPoint, showPoster= showPoster)
        return template , searchText

def generateSearch(searchText):

        showIDNum = tvShow.search_movie(searchText)
        del showIDNum[1:]
        showIDNum = str(showIDNum)
        showIDNum = showIDNum[11:]
        showIDNum = int(showIDNum.split("[")[0])

        GetShowData(showIDNum).getPoster()

        Show = GetShowData(showIDNum)
        DataPoint = Show.listSeriesData()
        ScaledYAxis, lastEp = getStats(DataPoint)

        showPoster = os.path.join(app.config['UPLOAD_FOLDER'], 'showPoster'+str(showIDNum)+'.jpg')
        template = render_template('index.html',processed_text = searchText, series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = DataPoint, showPoster = showPoster)
        return template , searchText


app = Flask(__name__)
showPosterFolder = os.path.join('static', 'showPoster')
app.config['UPLOAD_FOLDER'] = showPosterFolder

@app.route('/')

def index():
    #Index Page that graphs The Flash Data from above
    showPoster = os.path.join(app.config['UPLOAD_FOLDER'], 'showPoster.jpg')
    template = render_template('index.html',series = Show.getName(),finalEpNum = lastEp,minRatingFinal = ScaledYAxis , dataPoint = ShowDataPoint,showPoster = showPoster)
    return template



#When the user searches for a certain TV Show...
@app.route('/', methods=["GET", "POST"])

def my_form_post():

    #The users search results from HTML Page
    searchText = request.form['text']

    #If Change Graph is pressed
    if 'Change Graph' in request.form:
        #If user searches for an empty field, the page will default to grabbing The Flash data
        if (searchText ==''):
            return searchSite()
        return(generateSearch(searchText))

    #If Submit is pressed /static/showPoster
    if 'Submit' in request.form:
        if (searchText ==''):
            return searchSite()


        return(searchShow(searchText))
    
    if 'Home' in request.form:
        templateHome = render_template('home.html')
        return templateHome
        
    if 'SearchTab' in request.form:
        return searchSite()

    print(searchText)

    

    


#Start Web App
if __name__ == '__main__':
    app.run()

