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
        # display info
        print("Launching app01")

        # window stuffx
        self.window = _window
        self.window.overrideredirect(True)
        self.window.geometry(str(_appW) + "x" + str(_appH) + "+" + str(_appOffsetW) + "+0")

        # frames
        self.canvasVIDEO = Canvas(self.window, width = _appW / 2, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasCLASS = Canvas(self.window, width = _appW / 2, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="green")
        self.canvasVIDEO.pack(side = LEFT)
        self.canvasCLASS.pack(side = LEFT)

        # video capture
        self.video = VideoCapture(1, 1280, 720)

        # strobe image
        imgFolder = "D:/PERSO/_IMAGES/MSCOCO/train2014"
        self.imgPaths = self.getImgPaths(imgFolder)
        self.imgToDisplay = PIL.Image.open(self.imgPaths[0])
        self.canvasCLASS.create_image(self.canvasCLASS.winfo_width() * 0.5, self.canvasCLASS.winfo_height() * 0.5, image = self.imgToDisplay, anchor = CENTER)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1    # 30 fps
        self.update()
        self.window.mainloop()

    # update
    def update(self):
        # Get a frame from the video source
        ret, frame = self.video.get_frame()

        # display strob Image
        if random.random() < 0.8 :
            file = self.imgPaths[random.randint(0, len(self.imgPaths) - 1)]
            self.imgToDisplay = PIL.Image.open(file)
            self.canvasCLASS.create_image(self.canvasCLASS.winfo_width() * 0.5, self.canvasCLASS.winfo_height() * 0.5, image = self.imgToDisplay, anchor = CENTER)

        # display image
        if ret:
            frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvasVIDEO.create_image(self.canvasVIDEO.winfo_width() * 0.5, self.canvasVIDEO.winfo_height() * 0.5, image = frame, anchor = CENTER)

        # update app
        self.window.after(self.delay, self.update)

    # get images from folder
    def getImgPaths(self, _path):
        files = []
        for r, d, f in os.walk(_path):
            for file in f:
                files.append(os.path.join(r, file))
        return files

class VideoCapture:
    def __init__(self, _video_source, _camW, _camH):
        # Open the video source
        self.vid = cv2.VideoCapture(_video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", _video_source)

        # Set video size
        print("Setting up camera with input size [" + str(_camW) + "," + str(_camH) + "]")
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, _camW)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, _camH)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.rotate(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.ROTATE_90_CLOCKWISE))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def main():
    # parse arguments
    appOffsetW = int(sys.argv[1])
    appW = int(sys.argv[2])
    appH = int(sys.argv[3])

    # run App
    App(Tk(), appOffsetW, appW, appH)


if __name__ == "__main__":
    main()
