import PIL.Image, PIL.ImageTk
    import os
import numpy as np

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
            list.append(name)
    return list

# set variables
IMGW_MIN = 640
IMGH_MIN = 1080

# set folders
folderToPopulate = "D:/PERSO/_IMAGES/ALFRED/FULL_DATASET_PROCESSED/"
folderToProcess = "D:/PERSO/_IMAGES/ALFRED/FULL_DATASET"
fileNames = getImgPaths(folderToProcess)
filesListFull = [folderToProcess + "/" + f for f in fileNames]

# imagenet list
imageNetList = getLabelsFromFile("D:/TOAST/SPELAION/PYTHON/App/data/classesList.txt")
imageNetList = [el.replace(" ", "_").replace("'", "").lower() for el in imageNetList]

temp = []
for el in fileNames :
    el = el.split(".")[0]
    if el[-1] == '_' or el[-1] == '0':
        el = '_'.join(el.split("_")[:-1])
    el = el.lower()
    el = el.replace("'", "")
    temp.append(el)
fileNamesClean = temp

# set ratios
ratioMult = np.linspace(1.0, 1.5, 50, endpoint=True)

# get img size
count = 0
for nameInFolder, nameGood in zip(filesListFull, fileNamesClean):
    #print(nameInFolder + "\t" + nameGood)

    with PIL.Image.open(nameInFolder) as imgPil:
        imgWidth, imgHeight = imgPil.size

        if imgWidth < IMGW_MIN or imgHeight < IMGH_MIN :
            print("Not processing {} ({}x{})".format(nameGood, imgWidth, imgHeight))
            continue

        # compute new heights
        newW = 0
        newH = 0
        newWs = [int(IMGW_MIN * rat) for rat in ratioMult]
        newHs = [int(w * imgHeight / imgWidth) for w in newWs]

        for w, h in zip(newWs, newHs):
            if w >= IMGW_MIN and h >= IMGH_MIN:
                newW = w
                newH = h
                #print("{} => {}x{}".format(nameGood, w, h))
                break

        # compress
        ffmpegCmd = "ffmpeg.exe -i {} -compression_level 100 -vf scale={}:{} -loglevel panic {}.jpg".format(nameInFolder, newW, newH, folderToPopulate + nameGood)
        print("{} / 1000 - {}".format(count,  nameGood))
        os.system(ffmpegCmd)

        count += 1
