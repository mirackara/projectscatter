from imdb import IMDb
import random
import csv
import urllib.request
from bs4 import BeautifulSoup


# Create an instance of the IMDb class
tvShow = IMDb()



class GetShowData:

    def __init__(self,ID):
        self.ID = ID

       #Returns the name of show
    def getName(self):
        getName = tvShow.get_movie(self.ID)
        return getName
       #Gets Show Poster

    def getPoster(self):
        try:
            with urllib.request.urlopen('https://www.imdb.com/title/'+str(self.ID)+'/?ref_=fn_al_tt_1') as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                # Get url of poster image
                image_url = soup.find('div', class_='poster').a.img['src']
                # TODO: Replace hardcoded extension with extension from string itself
                extension = '.jpg'
                image_url = ''.join(image_url.partition('_')[0]) + extension
                filename = 'static/showPoster/showPoster' +str(self.ID)+'.jpg'
                with urllib.request.urlopen(image_url) as response:
                    with open(filename, 'wb') as out_image:
                        out_image.write(response.read())
                            
                # Ignore cases where no poster image is present
        except:
            with urllib.request.urlopen('https://www.imdb.com/title/tt0'+str(self.ID)+'/?ref_=fn_al_tt_1') as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
            # Get url of poster image
                image_url = soup.find('div', class_='poster').a.img['src']
                # TODO: Replace hardcoded extension with extension from string itself
                extension = '.jpg'
                image_url = ''.join(image_url.partition('_')[0]) + extension

                filename = 'static/showPoster/showPoster' +str(self.ID)+'.jpg'

                with urllib.request.urlopen(image_url) as response:
                    with open(filename, 'wb') as out_image:
                        out_image.write(response.read())
        print('Done with Poster!')
        


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
        seriesDataList = []
        tvShow.update(seriesName, 'episodes')
        try:
            totalSeasons = len(sorted(seriesName['episodes'].keys())) + 1
        except:
            return seriesDataList
        episodeCounter = 0
        ### Loops thru 'i' amount of Seasons.
        for i in range(1,totalSeasons):
          try:
            Season = seriesName['episodes'][i]
          except:
              return seriesDataList
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
            seriesDataList.append([episodeCounter, ratingFloat , ColorPicked])
        return  seriesDataList
