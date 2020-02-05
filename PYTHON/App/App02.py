# --------------------------------------------------------
#   APP02 of Collectif TOAST's ALFRED installation
#   This app receives the result of image classification
#   from App01 and displays corresponding picture from dataset
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# image
import PIL.Image, PIL.ImageTk
# OSC Server
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
# sound
from playsound import playsound
# misc
import time
import sys
import json
import os
import random

# App 02
class App:
    def __init__(self, _window, _config):
        # window stuffx
        self.window = _window
        self.window.title("APP02 - Image strob")
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"] + int(_config["appW"] * 1 / 3)
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))
        self.frameCount = 0
        self.prevTime = 0
        self.fps = 0

        # OSC server
        self.OSCAddr = _config["OSC_addr"]
        self.OSCPortApp02 = _config["OSC_port_App02"]

        # Set dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/changeImage", self.changeImage)

        # Launch OSC Server
        self.server = osc_server.ThreadingOSCUDPServer((self.OSCAddr, self.OSCPortApp02), self.dispatcher)
        self.serverThread = threading.Thread(target = self.server.serve_forever)
        self.serverThread.start()

        # canvas
        self.canvasCLASS = Canvas(self.window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg="black")
        self.canvasCLASS.pack(side = LEFT)

        # img stuff
        self.imgLabel = ""
        self.imgLabelOld = ""
        self.imgFolder = _config["imgFolder"]
        self.imgPaths = self.getImgPaths(self.imgFolder)
        self.imgPaths = [self.imgFolder + f for f in self.imgPaths]
        self.imgPosX = int(self.appW * 0.5)
        self.imgPosY = int(self.appH * 0.5)

        # display first img
        imgPath = self.imgPaths[0]
        self.imgToDisplay = PIL.Image.open(imgPath)
        self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)
        self.changeImg = False

        # conjard easter egg
        self.isConjard = _config["ConjardBool"]
        self.conjardStrength = _config["ConjardStrength"]

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 20    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        # compute fps
        currTime = time.time()
        deltaTime = currTime - self.prevTime
        self.fps = 1 / deltaTime

        # update image
        if self.changeImg == True:
            # display image
            file = self.imgFolder + self.imgLabel + ".jpg"
            self.imgToDisplay = PIL.Image.open(file)
            self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)
            self.canvasCLASS.create_image(self.imgPosX, self.imgPosY, image = self.imgToDisplay, anchor = CENTER)

        # update image change
        self.changeImg = False

        # compute delay time for fixed FPS
        elapsedUpdate = (time.time() - currTime) * 1000
        timeToDelay = int(self.delay - elapsedUpdate)
        timeToDelay = max(1, timeToDelay)

        # display info
        #print("[APP02] delay = {}\t{} fps".format(timeToDelay, int(self.fps)))

        # update loop
        self.frameCount += 1
        self.prevTime = currTime
        self.window.after(self.delay, self.update)

    def changeImage(self, unused_addr, args):
        self.changeImg = True
        self.imgLabel = args

        # easter conjard
        if self.isConjard :
            if random.random() <= self.conjardStrength :
                self.imgLabel = "african_hunting_dog"

        # check difference
        #if self.imgLabelOld != self.imgLabel:
            # random from folder
            #ind = int(random.random() * 20 + 1)
            #soundFile = "D:/PERSO/_SOUNDS/Eliot/B_E (" + str(ind) + ").wav"

            #
            #soundFile = "D:/PERSO/_SOUNDS/Pop_01.wav"

            #playsound(soundFile)

        self.imgLabelOld = self.imgLabel

        #print("[APP02] res = {}".format(self.imgLabel))

    # get images from folder
    def getImgPaths(self, _path):
        files = []
        for r, d, f in os.walk(_path):
            for file in f:
                if(file[0] == '.'):
                    continue
                files.append(file)
        return files

def main():
    # show info
    print("Running App02.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)

if __name__ == "__main__":
    main()
