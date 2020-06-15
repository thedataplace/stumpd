#! /usr/bin/python3
from ast import literal_eval
import datetime

# processing.py
# Takes unpacked files from Stumpd counters and turns them into open data

# Inputs:
#
#   "Metafile" - contains names and locations of counters
#   Directory tree containing counter files: tree.txt in the "processing" folder

# Outputs:
#
# The resultant data model is three dictionaries:
# Parks: { _Name_: [ParkID , Address, Description, Notes]}
# Counters: { _cindex_: [ParkID, number, location_text, lat, long]}
# Observations { _oindex_: [CounterID, date, time, triggers]}
#
# This is the "open data" output as it the most flexible.
# we can make the PCC Excel files out of it easily enough with a bit of input

# For now we will create the "Parks" table manually.
# The Counters table can be derived from the Metafile we already have.
# The Observations table is derived from the tree.txt file

# Note on naming conventions:
# Park code must be 3 letters.
# Counter ID is one letter plus 2 numbers. (I realise this will need to be amended in later versions)

# Parks table
parks = { "Devonport": ["DVP", "Devonport Park, Plymouth PL1 4BU", "Devonport Park", "first count November 2019"],
          "Hoe": ["HOE", "Osborne Place, Plymouth PL1 2PU", "The Hoe", "first count Christmas 2019"],
          "Central": ["CEN", "Central Park, Plymouth PL3 4HQ", "Central Park", "First count 2018"]
          }


# Counters table - read metafile    
with open("/Users/martinhowitt/Documents/Stumpd/processing/metafile") as metafile: 
    for line in metafile:
        # Title = ...
        if line[:5] == "Title":
            title = line[8:]
            print("Title: " + title)
        # Counter locations (location, lat, long)
        elif line[:9] == "Locations":
            locations = literal_eval(line[12:])

# Observations table
observations = {}
oindex = 1
with open("/Users/martinhowitt/Documents/Stumpd/processing/tree.txt") as tree:
    for line in tree:
        # if line contains a "/" it's a directory marker of the form DVP/L1/2019/09/18:
        # print("Length: ", len(line))
        if line[-2:] == ":\n": # this is a marker line, so read the variables
            day = line[-4:-2]
            month = line[-7:-5]
            year = line[-12:-8]
            date = str(day) + "-" + str(month) + "-" + str(year)
            location = line[0:-13]
            # counterid is a mash up of the park id + the counter number eg DVPL1
            if line[6] == "/":
                counterid = line[:3]+line[4:6]
            else:
                counterid = line[:3]+line[4:7]
        # if line finishes with ".TXT" it's a counter entry. format is hh-mm-ss.TXT
        elif line[-4:] == "TXT\n":
            ss = str(line[6:8])
            mm = str(line[3:5])
            hh = str(line[:2])
            time = hh + ":" + mm + ":" +ss
            date_time_str = date + " " + time
            date_time_obj = datetime.datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
            triggers = 1 # deprecated
            # write the table
            observations[oindex] = [counterid, str(date_time_obj.date()), str(date_time_obj.time()), triggers]
            oindex += 1
print(observations)

# write the tables to files....
# the "master" csv file is 3 files, one for each table

# parks.csv is name, ID string, address, description, more info
with open("/Users/martinhowitt/Documents/Stumpd/processing/parks.csv", "w") as parkfile:
    # line 1 contains headings
    parkfile.write("name, ID string, address, description, more info\n")
    for key in parks:
        outlst = parks[key]
        separator = ", "
        output = separator.join(outlst)
        parkfile.write(str(key) + ", " + output + "\n")

# counters.csv is index, park ID, Counter ID, location description, latitude, longitude
with open("/Users/martinhowitt/Documents/Stumpd/processing/counters.csv", "w") as countfile:
    # line 1 contains headings
    countfile.write("index, park ID, Counter ID, location description, latitude, longitude\n")
    for key in locations:
        loclst = locations[key]
        op = ""
        for item in range(len(loclst)):
            op += str(loclst[item])
            if item < (len(loclst) - 1):
                op += ", "
        countfile.write(str(key) + ", " + op + "\n")

# observations.csv is index, CounterID, date, time, triggers=1
with open("/Users/martinhowitt/Documents/Stumpd/processing/observations.csv", "w") as obsfile:
    # line 1 contains headings
    obsfile.write("index, CounterID, date, time, triggers\n")
    for key in observations:
        obslst = observations[key]
        op = ""
        for item in range(len(obslst)):
            op += str(obslst[item])
            if item < (len(obslst) - 1):
                op += ", "
        obsfile.write(str(key) + ", " + op + "\n")


                    
# push to open data platform
# re-zip the file and move to "archive"



