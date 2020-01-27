# --------------------------------------------------------
#   APP01 of Collectif TOAST's ALFRED installation
#   This app captures what a USB cam sees and perform
#   a classification every frame.
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# video / images
import cv2
import PIL.Image, PIL.ImageTk
# misc
import time
import sys
import os
import random

class App:
    # init
    def __init__(self, _window):
        # set window
        self.window = _window
        self.window.overrideredirect(True)
        self.appW = int(1920 / 3)
        self.appH = 1080
        self.offX = int(1920 * 4 / 3)
        self.offY = 0
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))

        # frames
        self.canvasImg = Canvas(self.window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasImg.pack(side = LEFT)

        # strobe image
        imgFolder = "D:/PERSO/_IMAGES/ALFRED/DATASET_50_IMAGES_TEST/_PROCESSED/"
        self.imgPaths = self.getImgPaths(imgFolder)
        self.imgPaths = [imgFolder + f for f in self.imgPaths]
        imgPath = self.imgPaths[0]
        self.imgToDisplay = PIL.Image.open(imgPath)
        self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    # update
    def update(self):
        # display strob Image
        if random.random() < 0.5 :
            file = self.imgPaths[random.randint(0, len(self.imgPaths) - 1)]
            self.imgToDisplay = PIL.Image.open(file)
            self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)
            self.canvasImg.create_image(self.canvasImg.winfo_width() * 0.5, self.canvasImg.winfo_height() * 0.5, image = self.imgToDisplay, anchor = CENTER)

        # update app
        self.window.after(self.delay, self.update)

    # get images from folder
    def getImgPaths(self, _path):
        files = []
        for r, d, f in os.walk(_path):
            for file in f:
                files.append(file)
        return files


def main():
    # run App
    App(Tk())


if __name__ == "__main__":
    main()
