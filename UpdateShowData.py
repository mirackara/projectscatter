import gzip
import shutil
import urllib.request

from GenerateShowData import *


def unzip(fileIn, fileOut):
    with gzip.open(fileIn, 'rb') as f_in:
        with open(fileOut, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def updateData():

    ratingsGet = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
    dataFullGet = 'https://datasets.imdbws.com/title.episode.tsv.gz'
    showNamesGet = 'https://datasets.imdbws.com/title.basics.tsv.gz'


    print("Updating Data Sets. This could take a while.")

    urllib.request.urlretrieve(ratingsGet, 'tempData/ratingsGet.tsv.gz')
    urllib.request.urlretrieve(dataFullGet, 'tempData/dataFullGet.tsv.gz')
    urllib.request.urlretrieve(showNamesGet, 'tempData/showNamesGet.tsv.gz')

    unzip("tempData/ratingsGet.tsv.gz", "ratings.csv")
    unzip("tempData/dataFullGet.tsv.gz", "dataFull.csv")
    unzip("tempData/showNamesGet.tsv.gz", "showNames.csv")

    getData()

    # Clean up temp files..


updateData()
