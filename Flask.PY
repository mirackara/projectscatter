from flask import Flask, request, url_for, redirect, render_template
from GetShowData import *


'''

class FlaskData:
    ......


'''

SeriesData = GetShowData('Community','3107288')
DataPoint = SeriesData.listSeriesData()
 
lastEp = DataPoint[-1][0]
Y = []
#Gets all Y's into a list
for i in range (0,lastEp):
    Y.append(DataPoint[i][1])

averageYRating = sum(Y) / len(Y)
averageYRating = round(averageYRating,2) 
ScaledYAxis = averageYRating - 3 
ScaledYAxis = round(ScaledYAxis, 2)
print(ScaledYAxis)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',Title = 'The Flash' )

@app.route('/Scatter', methods=['GET', 'POST'])
def Scatter():
    if request.method == 'POST':
        return redirect(url_for('index'))
    returnScatter = render_template('Scatter.html', series = SeriesData.getName() ,finalEpNum = lastEp ,minRatingFinal = ScaledYAxis ,dataPoint = DataPoint)

    return returnScatter


def run():
    if __name__ == '__main__':
        app.run()


run()
