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
    def __init__(self, _window, _appOffsetW, _appW, _appH):
        # window stuffx
        self.window = _window
        self.window.overrideredirect(True)
        self.window.geometry(str(_appW) + "x" + str(_appH) + "+" + str(_appOffsetW) + "+0")

        # frames
        self.canvasImg = Canvas(self.window, width = _appW, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasImg.pack(side = LEFT)

        # strobe image
        imgFolder = "D:/PERSO/_IMAGES/MSCOCO/train2014"
        self.imgPaths = self.getImgPaths(imgFolder)
        imgPath = self.imgPaths[0].replace("\\", '/')
        self.imgToDisplay = PIL.Image.open(imgPath)
        self.imgToDisplay = PIL.ImageTk.PhotoImage(self.imgToDisplay)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    # update
    def update(self):
        # display strob Image
        if random.random() < 1 :
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
                files.append(os.path.join(r, file))
        return files


def main():
    # run App
    App(Tk(), 1920, 1920, 1080)


if __name__ == "__main__":
    main()
