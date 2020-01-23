#!/usr/bin/env python3

# libs
from bs4 import BeautifulSoup
import requests
import random
import urllib.request
import urllib.parse
import time
import json
import os
from PIL import Image

# set variables
listFile = "imagenet.shortnames_short.list"
folderPath = "D:/TOAST/SPELAION/PYTHON/ImageScraping/folderToSave/"
#folderPath = "./test/"
numIm = 1
numItem = 0
imgMaxSize = 600
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

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

        # make directory
        try :
            os.mkdir(folderPath + querySavable + "/")
        except Exception as e:
            print(e)

        # url
        url = "https://www.google.co.in/search?q="+ queryUrl +"&source=lnms&tbm=isch"

        # display info
        print("{} / {} [{}] - {}".format(str(cnt+1), numItem, queryReadable, url))

        # get image links
        images = []
        tryId = 1
        while len(images) == 0:
            # sleep so not to spam server
            time.sleep(0.5)

            # fetch url
            try :
                r = urllib.request.urlopen(urllib.request.Request(url, headers=header), timeout=5)
            except Exception as e:
                print("CAN'T LOAD URL")

            # get soup
            soup = BeautifulSoup(r, 'html.parser')

            # display info
            print("\tTry #" + str(tryId) + " - " + str(r.getcode()))

            for a in soup.find_all("div",{"class":"rg_meta"}):
        	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        	    images.append((link,Type))

            if len(images) == 0:
                print("\t\tFOUND NO IMAGES. RETRYING...")
                tryId = tryId + 1

        # loop through images
        numSavedImage = 0
        for i , (img , Type) in enumerate(images):
            try:
                # fetch url
                print("\t\t" + img)
                print("\t\t\tLOADING")
                req = urllib.request.Request(img, headers=header)
                raw_img = urllib.request.urlopen(req, timeout=5).read()
                print("\t\t\tLOADED")

            # if error
            except Exception as e:
                #display info
                print("\t\t\tLOAD ERROR")
                #print(e)
                continue

                # set image name
            imgName = querySavable + "_"+ str(i)
            folderName = folderPath + querySavable + "/"
            extensionName = ""
            if len(Type)==0:
                extensionName = ".jpg"
            else :
                extensionName = "." + Type
            fullImgName = folderName + imgName + "_" + extensionName

            # save image
            f = open(fullImgName, 'wb')
            f.write(raw_img)
            f.close()

            # display info
            print("\t\t\tSAVING")

            # get size of image
            try:
                with Image.open(fullImgName) as imgPil:
                    imgWidth, imgHeight = imgPil.size

                # find new size
                ratio = imgWidth / imgHeight

                # set ffmpeg command
                ffmpegCmd = ""
                if(ratio >= 1):
                    ffmpegCmd = "ffmpeg.exe -i {0} -compression_level 100 -vf scale={2}:-1 -loglevel panic {1}.jpg".format(fullImgName, folderName + imgName, imgMaxSize)
                else:
                    ffmpegCmd = "ffmpeg.exe -i {0} -compression_level 100 -vf scale=-1:{2} -loglevel panic {1}.jpg".format(fullImgName, folderName + imgName, imgMaxSize)
                os.system(ffmpegCmd)
                os.remove(fullImgName)

                # display info
                print("\t\t\tRESIZING AND COMPRESSING")

                # iterate
                numSavedImage += 1
            except Exception as e:
                print("\t\t\tERROR WHILE FETCHING SIZE INFO")
                os.remove(fullImgName)

            # if we have saved enough images, we move onto next label
            if(numSavedImage == numIm):
                break

        # make thinks more readable
        print("\n")
