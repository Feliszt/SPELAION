# --------------------------------------------------------
#   MAINAPP of Collectif TOAST's ALFRED installation
#   This app runs app01 and app02 and kills them
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from  tkinter import *
# misc
import time
import sys
import subprocess
import time

class App:
    def __init__(self, _window):
        # window stuff
        self.window = _window

        # set window size
        winW = 400
        winH = 400
        winX = int(1920 * 0.5 - winW * 0.5)
        winY = int(1080 * 0.5 - winH * 0.5)
        winGeometry = "{}x{}+{}+{}".format(winW, winH, winX, winY)
        self.window.geometry(winGeometry)

        # frames
        runButton = Button(self.window, text="RUN", command=self.runApps)
        killButton = Button(self.window, text="STOP", command=self.killApps)
        runButton.pack()
        killButton.pack()

        # set App 01
        # app that runs VideoCapture and Image Classification
        # part 1 and 2 of ALFRED's tryptic
        self.runApp01 = "python.exe App01.py &"

        # set App 02
        # app that displays result images
        # part 2 of ALFRED's tryptic
        self.runApp02 = "python.exe App02.py &"

        # set App 03
        # app that runs GAN
        # part 3 of ALFRED's tryptic
        self.runApp03 = "python.exe App03.py &"

        # run both apps
        self.runApps()

        self.window.protocol("WM_DELETE_WINDOW", self.killMainApp)
        self.window.mainloop()

    def runApps(self):
        self.app01 = subprocess.Popen(self.runApp01)
        self.app02 = subprocess.Popen(self.runApp02)
        self.app03 = subprocess.Popen(self.runApp03)

    def killApps(self):
        print("Killing apps.\n")
        self.app01.kill()
        self.app02.kill()
        self.app03.kill()

    def killMainApp(self):
        self.killApps()
        self.window.destroy()

def main():
    # run App
    App(Tk())


if __name__ == "__main__":
    main()
