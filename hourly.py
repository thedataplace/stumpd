# hourly.py
#
# converts observations.csv into hourly counts for PCC reporting
#
# observations.csv is found in ../processing/observations.csv
# format is id, counterID, date, time, trigger count
import csv


results = []
with open("observations.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader: # each row is a list
        # if row is header then ignore
        if row[0] == 'index': 
            newrow = ['Counter', 'year', 'month', 'day', 'hour', 'count']
            results.append(newrow)
            continue;
        # otherwise process
        newrow = []
        counter = row[1]
        year = int(row[2][0:5])
        month = int(row[2][6:8])
        day = int(row[2][9:11])
        hour = int(row[3][1:3])
        count = 1
        newrow = [counter, year, month, day, hour, count]
        results.append(newrow)

csvfile.close()

# "results" is now a list of lists
# for each list, compare with the previous one and if items 0 - 4 are identical, add item 5 from the previous list, then delete the previous list
# this won't work if items are out of sequence, so will do a clean up once numbers are manageable

output = []

for n in range(len(results)):
# for n in range(100):
    
    if (n == 0):
        output.append(results[n])
        continue;
    # set up table

    else:
        entry = results[n]
        output.append(entry)

        if (len(output) > 1):
            previous = output[-2]
        else:
            previous = output[-1]

        if entry[0:5] == previous[0:5]:
            entry[5] += previous[5]
            output[-1] = entry
            del output[-2]

with open('hourly-obs-csv.csv', 'w', newline='') as csvfile:
    handler = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for n in range(len(output)):
        handler.writerow(output[n])

csvfile.close()

# final format is a dictionary
# {date1: {h1:c1, h2:c2, h3:c3, h4:c4 .... , h24:c24}, date2: {h1: c1, ... h24: c24}, ...,daten: { ... }}
# so for each line in the output, what date is it, what hour was it, and what count was it
# we'll need to initialise the lists so they are fixed length = 24

dictout = {}

for n in range(len(output)):

    if (n > -1):
        # what is the date. make it a single string by concatenating
        datenum = str(output[n][3]) + "/" + str(output[n][2]) + "/" + str(output[n][1])
        keyexists = dictout.get(datenum, -1)

        hour = int(output[n][4])
        count = int(output[n][5])
        newdata = {hour: count}

        # if datenum is already in dictout, add the entry to it, otherwise it's a new entry
        if keyexists == -1:
            dictout[datenum] = newdata
        else:
            dictout[datenum].update(newdata)

#
# to do: identify the index of the highest count in each day
#
# print(dictout)
for key in dictout:
    values = (dictout[key])
    maxkey = max(values, key=values.get)
    print("highest hour for ", key, " is ", maxkey) 

with open('hourlyfinal.csv', 'w', newline='') as finalcsv:
    handler = csv.writer(finalcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # write column headings as dates    
    dates = list(dictout.keys())
    handler.writerow(dates)
    
    for n in range(24):
        outrow = [0] * len(dates)
        for i in range(len(dates)):
            entry = dictout.get(dates[i])
            outrow[i] = entry.get(n)

        handler.writerow(outrow)

finalcsv.close()
