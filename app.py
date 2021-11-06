from flask import Flask, request, render_template, make_response
from flask_restful import Api, Resource
from UpdateShowData import updateData
from sendShowData import getShowData
from copy import deepcopy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///showDatabase.db'  ## TO-DO: Retire CSV and convert into SQL Database

#  Status Codes
#  200 = Found Show
#  404 = Show Not Found


@app.route('/search')
##  handles GET/PUT requests any time a new show is searched
class showInfo(Resource):  
    def get(self, showName):
        statusCode = 0
        try:  # Show Found!
            seasons = 0
            bestEpName = ""
            worstEpName = ""
            bestEpRating = 0.0
            worstEpRating = 0.0
            showData, seasons, bestEpName, bestEpRating, worstEpName, worstEpRating = getShowData(
                showName, seasons, False)
            statusCode = 200
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html', statusCode=statusCode, showData=showData,
            seasons=seasons, bestEpName=bestEpName, bestEpRating=bestEpRating,
            worstEpName=worstEpName, worstEpRating=worstEpRating), 200, headers)
        except:  # Show not found..
            print("error")
            headers = {'Content-Type': 'text/html'}
            statusCode = 404
            return make_response(render_template('home.html', statusCode=statusCode, showData={}, seasons=0), 200, headers)

    def put(self, showName):
        print(request.form['Schitt\'s Creek'])
        return {}

api.add_resource(showInfo, "/search/<string:showName>")

##  Runs index() for homepage
@app.route('/')
def index():
    seasons = 0
    bestEpName = ""
    worstEpName = ""
    bestEpRating = 0.0
    worstEpRating = 0.0
    showData, seasons, bestEpName, bestEpRating, worstEpName, worstEpRating = getShowData(
        "Schitt's Creek", seasons, False)
    statusCode = 200
    return render_template('home.html', statusCode=statusCode, showData=showData,
    seasons=seasons, bestEpName=bestEpName, bestEpRating=bestEpRating,
    worstEpName=worstEpName, worstEpRating=worstEpRating)


showNames = []
@app.route('/compare')
##  handles GET/PUT requests any time a new show is compared

class showInfoCompare(Resource):
    def get(self, showName):
        showNames = showName.split('+')
        while("" in showNames):
            showNames.remove("")
        print(showNames)

        try:  # Show Found!
            print(showName)

            testList = []
            numOfShows = 0
            for show in showNames:
                numOfShows += 1
                seasons = 0
                showData, seasons = getShowData(show, seasons, True)
                testList.append(deepcopy(showData))

            return make_response(render_template('multigraph.html', test=testList, numOfShows=numOfShows, lastShowAdded = 'true'))
        except:  # Show not found..
            print("error")
            return make_response(render_template('multigraph.html', test=testList, numOfShows=numOfShows, lastShowAdded = 'false'))

    def put(self, showName):
        print(request.form["Schitt's Creek"])
        return {}


api.add_resource(showInfoCompare, "/compare/<string:showName>")



# Start Web App, update ratings
if __name__ == '__main__':
    #updateData()
    app.run()
