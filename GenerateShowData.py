import csv
import operator
import itertools

data = csv.reader(open('dataFull.csv'),delimiter='\t')
sortedlist = sorted(data, key=operator.itemgetter(1), reverse=False)



ratings = csv.reader(open('ratings.csv'), delimiter = '\t')
tconstRatings = {}
for row in ratings:
    tconstRatings[row[0]] = row[1] 

rawShowNames = open("showNames.csv", 'r', encoding  = "utf-8")
showNamesCSV = csv.reader(rawShowNames, delimiter = '\t')
epNames = {}
showNames = {}
for row in showNamesCSV:
    if row[1] != "short" or row[1] != "movie":
        epNames[row[0]] = row[3]


with open('dataFullSorted.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    counter = 0
    for row in sortedlist:
        counter =+ 1
        tconst = row[0] # tconst = episodeID
        if row[2] == "\\N": 
            continue
        if tconst in tconstRatings: # If a rating exists for a given episode
            row.append(tconstRatings[tconst]) # Add the rating to the row
            if tconst != "tconst":
                row.append(epNames[tconst]) # Adds the episode name to the row
                if row[1] in epNames:
                    row[1] = epNames[row[1]]
            writer.writerow(row)



