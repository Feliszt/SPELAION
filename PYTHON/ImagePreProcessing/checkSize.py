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

# set variables
IMGW_MIN = 640
IMGH_MIN = 1080

# set folder for results
folderToPopulate = "D:/PERSO/_IMAGES/ALFRED/DATASET_50_IMAGES_TEST/_PROCESSED/"

# get list of files
folderToProcess = "D:/PERSO/_IMAGES/ALFRED/DATASET_50_IMAGES_TEST"
filesListFull = [folderToProcess + "/" + f for f in getImgPaths(folderToProcess)]

# set ratios
ratioMult = np.linspace(1.0, 1.5, 20, endpoint=True)

# show info
print(folderToProcess)

# get img size
for f in filesListFull:
    # get file name only
    fileName = f.split('/')[-1]
    fileName = fileName.split('.')[0]

    with PIL.Image.open(f) as imgPil:
        imgWidth, imgHeight = imgPil.size

        if imgWidth < IMGW_MIN or imgHeight < IMGH_MIN :
            print("Not processing {}\n".format(fileName))
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
                #print("{}x{}".format(w, h))
                break

        # show info
        print("{}\n\t{}x{} => {}x{}".format(fileName, imgWidth, imgHeight, newW, newH))

        # compress
        ffmpegCmd = "ffmpeg.exe -i {} -compression_level 100 -vf scale={}:{} -loglevel panic {}.jpg".format(f, newW, newH, folderToPopulate + fileName + "_rs")
        os.system(ffmpegCmd)

        #
        print("\n")
