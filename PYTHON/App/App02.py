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
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"] + int(_config["appW"] * 1 / 3)
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))

        # canvas
        self.canvasCLASS = Canvas(self.window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg="green")
        self.canvasCLASS.pack(side = LEFT)

        # img stuff
        self.imgFolder = "D:/PERSO/_IMAGES/ALFRED/DATASET_50_IMAGES_TEST/_PROCESSED/"
        self.imgPaths = self.getImgPaths(self.imgFolder)
        self.imgPaths = [self.imgFolder + f for f in self.imgPaths]
        self.imgPosX = int(self.appW * 0.5)
        self.imgPosY = int(self.appH * 0.5)

        # display first img
        imgPath = self.imgPaths[0]
        self.imgToDisplay = PIL.Image.open(imgPath)
        self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 16    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        # display strob Image
        if random.random() < 0.5 :
            file = self.imgPaths[random.randint(0, len(self.imgPaths) - 1)]
            self.imgToDisplay = PIL.Image.open(file)
            self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)
            self.canvasCLASS.create_image(self.imgPosX, self.imgPosY, image = self.imgToDisplay, anchor = CENTER)

        self.window.after(self.delay, self.update)

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
    with open('config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
