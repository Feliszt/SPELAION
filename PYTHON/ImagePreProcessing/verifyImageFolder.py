import os

# get images from folder
def getImgPaths(_path):
    files = []
    for r, d, f in os.walk(_path):
        for file in f:
            if(file[0] == '.'):
                continue
            files.append(file)
    return files

# get indexes
def getLabelsFromFile(_fileName) :
    list = []
    with open(_fileName, "r") as classesFile:
        while True:
            line = classesFile.readline()
            if not line:
                break
            line = line.strip()
            name = line.split(',')[0]
            name = name.replace(' ', '_')
            name = name.replace("'", "")
            name = name.lower()
            list.append(name)
    return list

# imageFolder
imageNames = getImgPaths("D:/PERSO/_IMAGES/ALFRED/FULL_DATASET_PROCESSED/")
imageNames = [el.split('.')[0] for el in imageNames]

# image net labels
imageNetLabels = getLabelsFromFile("D:/TOAST/SPELAION/PYTHON/App/data/classesListFull.txt")

#
for el in  imageNames:
    if el not in imageNetLabels :
        print(el)
