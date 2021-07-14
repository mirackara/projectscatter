from flask import Flask, request, render_template, make_response
from sendShowData import *
from copy import deepcopy

app = Flask(__name__)

@app.route('/')



def index():
    showNames = ["Superstore", "Breaking Bad", "Family Guy"]
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

#Start Web App
if __name__ == '__main__':
    app.run(debug=True)


