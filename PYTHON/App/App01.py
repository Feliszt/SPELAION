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
import json

# App 01
class App:
    def __init__(self, _window, _config):
        # set window
        self.window = _window
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"]
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))

        # cam stuff
        self.camIndex = _config["camIndex"]
        self.camW = _config["camW"]
        self.camH = _config["camH"]
        self.camPosX = int(self.appW * 0.5)
        self.camPosY = int(self.appH * 0.5)
        self.cam = VideoCapture(self.camIndex, self.camW, self.camH)

        # Create a canvas that can fit the above video source size
        self.canvasVIDEO = Canvas(_window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg='red')
        self.canvasVIDEO.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 16
        self.update()

        # run main loop
        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.cam.get_frame()
        if ret:
            self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvasVIDEO.create_image(self.camPosX, self.camPosY, image = self.img, anchor = CENTER)

        self.window.after(self.delay, self.update)

# video capture class
class VideoCapture:
    def __init__(self, _video_source, _camW, _camH):
        # Open the video source
        self.cam = cv2.VideoCapture(_video_source)
        if not self.cam.isOpened():
            raise ValueError("Unable to open video source", _video_source)
        else:
            print("Setting up camera with input size [" + str(_camW) + "," + str(_camH) + "] successful")

        # Set video size
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, _camW)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, _camH)

        # Get video source width and height
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # get frame
    def get_frame(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.rotate(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.ROTATE_90_CLOCKWISE))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cam.isOpened():
            self.cam.release()

def main():
    # show info
    print("Running App01.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
