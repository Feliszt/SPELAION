import os
from os import listdir
from os.path import isfile, join
import shutil

# get indexes
def populateList(fileName) :
    count = 0
    list = []
    with open(fileName, "r") as classesFile:
        while True:
            count += 1
            line = classesFile.readline()
            if not line:
                break
            line = line.strip()
            #print("{}: {}".format(count, line.strip()))
            name = line.split(',')[0]
            list.append(name)
    return list

#
folder = "D:/PERSO/_IMAGES/ImageNet/"
imageNetListFolder = "D:/TOAST/SPELAION/PYTHON/App/data/classesList.txt"
folderToPopulate = "D:/PERSO/_IMAGES/ImageNet_1000/"

# labels
imageNetList = populateList(imageNetListFolder)
imageNetList = [f.replace(' ', '_').lower() for f in imageNetList]

# folders
folders = listdir(folder)
foldersFull = [folder + f for f in folders]
folders = [f.replace(' ', '_').replace("'", "").lower() for f in folders]

# compare
labelToFolder = []
for label in imageNetList:
    # get index of label and store it
    ind = folders.index(label)
    labelToFolder.append((label, foldersFull[ind]))

for el in labelToFolder:
    folder = el[1] + '/'
    for f in listdir(folder):
        fileName = folder + f
        if(os.path.isfile(fileName)):
            fileNameDest = folderToPopulate + el[0] + ".jpg"
            shutil.copyfile(fileName, fileNameDest)
