from flask import Flask, request, render_template, make_response
from flask_restful import Api, Resource
from sendShowData import *
from copy import deepcopy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///showDatabase.db'



class showInfo(Resource): # Resource Class that handles GET/PUT/POST Requests
    def get(self,showName):
        statusCode = 0
        try: # Show Found!
            seasons = 0
            bestEpName = ""
            worstEpName = ""
            bestEpRating = 0.0
            worstEpRating = 0.0
            showData, seasons, bestEpName , bestEpRating, worstEpName, worstEpRating = getShowData(showName,seasons)
            statusCode = 200
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html', statusCode = statusCode, showData = showData, seasons = seasons, bestEpName = bestEpName, bestEpRating = bestEpRating, worstEpName = worstEpName, worstEpRating = worstEpRating),200,headers)
        except: # Show not found..
            print("error")
            headers = {'Content-Type': 'text/html'}
            statusCode = 404
            return make_response(render_template('home.html',statusCode = statusCode, showData = {}, seasons = 0),200,headers)
    
    def put(self,showName):
        print(request.form['Schitt\'s Creek']) 
        return {}
    

api.add_resource(showInfo, "/search/<string:showName>")
@app.route('/')
def index():
    seasons = 0
    bestEpName = ""
    worstEpName = ""
    bestEpRating = 0.0
    worstEpRating = 0.0
    showData, seasons , bestEpName , bestEpRating, worstEpName, worstEpRating = getShowData("Schitt's Creek",seasons)
    statusCode = 200
    return render_template('home.html', statusCode = statusCode, showData = showData, seasons = seasons , bestEpName = bestEpName, bestEpRating = bestEpRating, worstEpName = worstEpName, worstEpRating = worstEpRating)


@app.route('/search')
def search():
    return 'Search'
showNames = []



class showInfoCompare(Resource): # Resource Class that handles GET/PUT/POST Requests
    def get(self,showName):
        statusCode = 0
        try: # Show Found!
            print(showName)
            showNames = showName.split('+') 
            while("" in showNames) :
                showNames.remove("")
            print(showNames)

            testList = []
            numOfShows = 0
            for show in showNames:
                numOfShows+= 1
                seasons = 0
                bestEpName = ""
                worstEpName = ""
                bestEpRating = 0.0
                worstEpRating = 0.0
                showData, seasons, bestEpName, worstEpName, bestEpRating, worstEpRating = getShowData(show,seasons)
                testList.append(deepcopy(showData))

            return make_response(render_template('multigraph.html', test = testList, numOfShows = numOfShows))
        except: # Show not found..
            print("error")
            headers = {'Content-Type': 'text/html'}
            statusCode = 404
            return make_response(render_template('home.html',statusCode = statusCode, showData = {}, seasons = 0),200,headers)
    
    def put(self,showName):
        print(request.form['Schitt\'s Creek']) 
        return {}
    

api.add_resource(showInfoCompare, "/compare/<string:showName>")
@app.route('/')
def indexCompare():
    testList = []
    numOfShows = 0
    for show in showNames:
        numOfShows+= 1
        seasons = 0
        bestEpName = ""
        worstEpName = ""
        bestEpRating = 0.0
        worstEpRating = 0.0
        showData, seasons, bestEpName , bestEpRating, worstEpName, worstEpRating = getShowData(show,seasons)
        testList.append(deepcopy(showData))

    return make_response(render_template('multigraph.html', test = testList, numOfShows = numOfShows))

@app.route('/compare')
def compare():
    return 'compare'

#Start Web App
if __name__ == '__main__':
    app.run(debug=True)
