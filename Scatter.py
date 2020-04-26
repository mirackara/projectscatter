import matplotlib.pyplot as plt 
import numpy as np
from imdb import IMDb
import os.path
import random
import csv
from flask import Flask, request, render_template
import random
import os

# create an instance of the IMDb class
tvShow = IMDb()
#Community : 1439629
#Breaking Bad : 0903747
#Game of Thrones : 0944947
#Simpsons : 0096697

series = tvShow.get_movie('1439629')

print('Catalogging', series)

tvShow.update(series, 'episodes')
allSeasons = sorted(series['episodes'].keys())
episodes = series.get('episodes')

allsznRating = []
allsznNum = []
dataTest = []



counterNum = 0
counterNumFirst = 0





def ratingGrabber(s):
  epNum = []
  epRating = []
  for i in range(1,len(s)+1):
    epRating.append(s[i]['rating'])
    epNum.append(i)
  return epRating, epNum

def seasonColorPicker():
  random_number = random.randint(0,16777215)
  hex_number = str(hex(random_number))
  hex_number ='#'+ hex_number[2:]

  return hex_number

def graph(x,y):
  plt.scatter(x,y, label='Episode', color=color, s=30, marker="o")


fileName = str(series)+"Data"+ ".csv"
f = open(str(fileName),'a')
f.write('epNum,Rating \n')

if (os.path.isfile(fileName) == True ):
  print('File already exists!')
  print('Skipping to starting flask...')
  
for i in range(1,len(allSeasons)+1):
  Season = series['episodes'][i]
  SeasonRatings = ratingGrabber(Season)[0]
  allsznRating.append(SeasonRatings)
  sNum = ratingGrabber(Season)[1]  
  ratingLength = int(len(sNum))
  allsznNum.append(sNum)
  counterNumFirst = counterNum 
  counterNum = counterNum + ratingLength
  x = list(range(counterNumFirst,counterNum))
  r = random.random()
  b = random.random()
  g = random.random()
  color = (r, g, b)
  graph(x,SeasonRatings)
  colorPicked = seasonColorPicker()
  for i in range(1,len(sNum)):
      #i = episode number
    if (i == len(sNum)-1):
      f.write("")
      #f.write('New Season \n') THIS WILL DIVIDE THE SEASONS UP IN CSV AND 
      
    rating = str(round(SeasonRatings[i],1))
    epNum = str(x[i])
    i = int(epNum)
    #dataTest.append([i,float(round(SeasonRatings[i],1)), "0000ff"])
    print(i)
    fOut = (epNum + ',' +rating + '\n')
    dataTest.append([int(epNum), float(rating),str(colorPicked)])
    f.write(fOut)
    
  finalEpNum = epNum
  plt.plot(np.unique(x), np.poly1d(np.polyfit(x, SeasonRatings, 1))(np.unique(x)),color=color)

minRatingList = (min(allsznRating))
minRatingFinal = (min(minRatingList)) - 1 
figName = str(series) + ".png"
plt.ylabel("Rating")
plt.xlabel("Episode")
plt.title(series)
plt.ylim(minRatingFinal, 10)
plt.savefig(figName)
f.close()
print('final ep : ', finalEpNum)

with open(fileName, 'r') as file:
    data = file.read().replace('(', '')
    data = data.replace(')', '\n')
f = open(str(fileName),'w')
f.write(data)
f.close()
print(dataTest)
app = Flask(__name__)
@app.route('/')
def SendtoHTML():
    finalEpNumParsable = int(finalEpNum)
    datapointTest = [[1, 8.7, "0000ff"],[2, 6.7, "orange"],[3, 8.7, "0000ff"],[4,6.7,'red']]
    render = render_template('Scatter.html', series = series,finalEpNum = finalEpNumParsable,minRatingFinal = minRatingFinal ,dataPoint = dataTest,season1 = datapointTest)
    return render

def run():
    if __name__ == '__main__':
        app.run()


run()



