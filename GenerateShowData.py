####  GenerateShowData.py  
####  Rearrange and combine data pulled from IMDB's Database into a singular CSV
import csv
import operator

def getData():

    ##  dataFull.csv = [tconst, parentTconst, seasonNumber, episodeNumber]
    ##                 (episode ID), (TV Show ID)
    data = csv.reader(open('dataFull.csv'), delimiter='\t')
    sortedlist = sorted(data, key=operator.itemgetter(1), reverse=False)

    ##  ratings.csv = [tconst, averageRating, numVotes]
    ##  Only need tconst and averageRating
    ratings = csv.reader(open('ratings.csv'), delimiter='\t')
    tconstRatings = {}
    for row in ratings:
        tconstRatings[row[0]] = row[1] #  tconstRatings["tconst"] = averageRating

    ##  showNames.csv = [tconst, titleType, primaryTitle, originalTitle, isAdult,
    ##  startYear, endYear, runtimeMinutes, genres]
    rawShowNames = open("showNames.csv", 'r', encoding="utf-8")
    showNamesCSV = csv.reader(rawShowNames, delimiter='\t')
    rawShowNames.close()
    epNames = {}

    ##  Cleaning up showNames a bit by removing any movies or short-movies
    for row in showNamesCSV:
        if row[1] != "short" or row[1] != "movie":
            epNames[row[0]] = row[3]  ##  epNames[tconst] = originalTitle

    ##  Combine rearranged data into empty showdata csv
    ##  showData.csv = [tconst, parentTconst, seasonNumber, episodeNumber, averageRating]
    with open('showdata.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in sortedlist:
            tconst = row[0]  ## tconst = episodeID
            if row[2] == "\\N":
                continue
            if tconst in tconstRatings:  ##  If a rating exists for a given episode
                row.append(tconstRatings[tconst])  ##  Add the rating to the row
                if tconst != "tconst":
                    ##  Adds the episode name to the row
                    row.append(epNames[tconst])
                    if row[1] in epNames:
                        row[1] = epNames[row[1]]
                writer.writerow(row)
