#!/usr/bin/env python3

# libs
import requests
import random
import urllib.request
import time

# set variables
listFile = "imagenet.shortnames_short.list"
folderPath = "D:/PERSO/_IMAGES/ImageNet/"
numIm = 1

with open(listFile, 'r') as f:
    for cnt, line in enumerate(f):

        # sleep so not to spam server
        time.sleep(2)

        # get query
        query = line.strip()

        # Search the web for the first image
        r = requests.get("https://api.qwant.com/api/search/images",
           params={
               'count': 5,
               'q': query,
               't': 'images',
               'safesearch': 0,
               'locale': 'en_US',
               'uiv': 4
           },
           headers={
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
           }
        )
        print(r)

        comment = '''
        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]


        for i in range(numIm):
            print(i)


            url = urls[i]

            print("{} - {}".format(query, url))

            # save to disk
            destination = folderPath + query.replace(" ", "_") +
            urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")'''
