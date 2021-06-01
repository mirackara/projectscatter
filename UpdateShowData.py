import csv
import urllib.request
import gzip
import shutil
import os
from GenerateShowData import *

def unzip(fileIn, fileOut):
    with gzip.open(fileIn, 'rb') as f_in:
        with open(fileOut, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


ratingsGet = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
dataFullGet = 'https://datasets.imdbws.com/title.episode.tsv.gz'
showNamesGet = 'https://datasets.imdbws.com/title.basics.tsv.gz'


print("Updating Data Sets")

urllib.request.urlretrieve(ratingsGet, 'tempData/ratingsGet.tsv.gz')
urllib.request.urlretrieve(dataFullGet, 'tempData/dataFullGet.tsv.gz')
urllib.request.urlretrieve(showNamesGet, 'tempData/showNamesGet.tsv.gz')

unzip("tempData/ratingsGet.tsv.gz", "ratings.csv")
unzip("tempData/dataFullGet.tsv.gz", "dataFull.csv")
unzip("tempData/showNamesGet.tsv.gz", "showNames.csv")

getData()

# Clean up temp files..
print("Cleaning Up Files...")
os.remove('tempData/ratingsGet.tsv.gz')
os.remove('tempData/dataFullGet.tsv.gz')
os.remove('tempData/showNamesGet.tsv.gz')
os.remove('ratings.csv')
os.remove('showNames.csv')
os.remove('dataFull.csv')