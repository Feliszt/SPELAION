#!/usr/bin/env python3

# set variables
listFile = "imagenet.shortnames_1000.list"
urlTemplate = "https://www.bing.com/images/search?&q={0}&qft=+filterui:imagesize-custom_1280_2160+filterui:licenseType-Any"
numItem = 0

#
fileToWrite = open("nameList.txt", "a")

# get number of lines
with open(listFile) as f:
    for i, l in enumerate(f):
        pass
    numItem = i + 1

# loop line by line
with open(listFile, 'r') as f:
    for cnt, line in enumerate(f):
        # get query
        queryReadable = line.strip()
        querySavable = queryReadable.replace(' ', '_').replace('/', '-')
        queryUrl ='+'.join(queryReadable.split())

        fileToWrite.write("-------------------\n")
        fileToWrite.write("\n")
        fileToWrite.write("{0} / {1}\n".format(cnt+1, numItem))
        fileToWrite.write(querySavable + "\n")
        fileToWrite.write(urlTemplate.format(queryUrl) + "\n")
        fileToWrite.write("\n")

fileToWrite.close()
