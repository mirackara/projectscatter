from imdb import IMDb
import random
from flask import Flask, request, url_for, redirect, render_template
import random



# Create an instance of the IMDb class 
tvShow = IMDb()



class GetShowData:
    
    def __init__(self,Name,ID):
        self.Name = Name
        self.ID = ID
        
       #Returns the name of show
    def getName(self):
        getName = tvShow.get_movie(self.ID)
        return getName

       #Returns Both Episode Data and Rating Data
    def seriesDataGrabber(self,Season):
        epNum = []
        epRating = []

        for i in range(1,len(Season)+1):
            try:
                epRating.append(Season[i]['rating'])
                epNum.append(i)
            except:
                return epRating, epNum

        return epRating, epNum


    def seasonColorPicker(self):
      random_number = random.randint(0,16777215)
      hex_number = str(hex(random_number))
      hex_number ='#'+ hex_number[2:]

      return hex_number


       #Returns Total Episodes and Ratings numbered in list.
    def listSeriesData(self):
        seriesName = GetShowData.getName(self)
        tvShow.update(seriesName, 'episodes')
        totalSeasons = len(sorted(seriesName['episodes'].keys())) + 1
        seriesDataList = []
        allEpRatings = []
        episodeCounter = 0
        episodeCounterList = []
        ### Loops thru 'i' amount of Seasons.
        for i in range(1,totalSeasons):
          Season = seriesName['episodes'][i]
          ColorPicked = GetShowData.seasonColorPicker(self)
         
         ##Episode
          epNum = GetShowData.seriesDataGrabber(self,Season)[1]          
          ## [1,2,3,...,X]

          ##Rating

          SeasonRatings = GetShowData.seriesDataGrabber(self,Season)[0]
          ## [9.45,6.46,7.45,...,Y]

          # Loops through 'i' amount of Episodes.
          for i in range(1,len(epNum)+1):
            episodeCounter+=1
            ratingFloat = float(SeasonRatings[i-1])
            ratingFloat = round(ratingFloat, 2)
            print(ratingFloat)
            seriesDataList.append([episodeCounter, ratingFloat ,str(ColorPicked)])
        return  seriesDataList
    


'''

class FlaskData:
    ......


'''
FlashData = GetShowData('The Flash','3107288')
DataPoint = FlashData.listSeriesData()
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
    returnScatter = render_template('Scatter.html', series = FlashData.getName() ,finalEpNum = lastEp ,minRatingFinal = ScaledYAxis ,dataPoint = DataPoint)

    return returnScatter


def run():
    if __name__ == '__main__':
        app.run()


run()


