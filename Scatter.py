import json
import requests
import matplotlib.pyplot as plt 
import numpy as np
from numpy.polynomial.polynomial import polyfit
from imdb import IMDb

import random
import csv
import itertools 
from flask import Flask, request, render_template
import random
import os




# create an instance of the IMDb class
ia = IMDb()
#Community : 1439629
#Breaking Bad : 0903747
#Game of Thrones : 0944947
#Simpsons : 0096697
series = ia.get_movie('1439629')
print(series)
ia.update(series, 'episodes')
allSeasons = sorted(series['episodes'].keys())
episodes = series.get('episodes')

allsznRating = []
allsznNum = []
counterNum = 0
counterNumFirst = 0
def ratingGrabber(s):
  epNum = []
  epRating = []
  for i in range(1,len(s)+1):
    epRating.append(s[i]['rating'])
    epNum.append(i)
  return epRating, epNum
def graph(x,y):
  plt.scatter(x,y, label='Episode', color=color, s=30, marker="o")
fileName = str(series)+"Data"+ ".csv"
f = open(str(fileName),'a')

for i in range(1,len(allSeasons)+1):
  s = series['episodes'][i]
  sRating = ratingGrabber(s)[0]
  allsznRating.append(sRating)

  sNum = ratingGrabber(s)[1]
  ratingLength = int(len(sNum))
  allsznNum.append(sNum)
  counterNumFirst = counterNum 
  counterNum = counterNum + ratingLength
  x = list(range(counterNumFirst,counterNum))
  r = random.random()
  b = random.random()
  g = random.random()
  color = (r, g, b)
  graph(x,sRating)


  for i in range(1,len(sNum)):
      #i = episode number
    fOut = (x[i], round(sRating[i],1))
    f.write(str(fOut))
    if (i == len(sNum)-1):
      f.write(",")
  finalEpNum = fOut[0]
  plt.plot(np.unique(x), np.poly1d(np.polyfit(x, sRating, 1))(np.unique(x)),color=color)

minRatingList = (min(allsznRating))
minRatingFinal = (min(minRatingList)) - 1 
figName = str(series) + ".png"
plt.ylabel("Rating")
plt.xlabel("Episode")
plt.title(series)
plt.ylim(minRatingFinal, 10)
plt.savefig(figName)
f.close()


with open(fileName, 'r') as file:
    data = file.read().replace('(', '[')
    data = data.replace(')', ']')
    data = data.replace('][', '],[')

f = open(str(fileName),'w')
f.write(data)
f.close()

app = Flask(__name__)
@app.route('/')
def hello_world():
    x = [0.2]
    y = [0.4]
    finalEpNumSpaced = finalEpNum + 10

    return render_template('Scatter.html', x = x, y = y, series = series,finalEpNum = finalEpNumSpaced,minRatingFinal = minRatingFinal)


if __name__ == '__main__':
    app.run()
