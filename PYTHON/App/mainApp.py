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

        # set App 01
        # app that runs VideoCapture and Image Classification
        # part 1 and 2 of ALFRED's tryptic
        self.runApp01Cmd = "python.exe App01.py &"

        # set App 02
        # app that displays result images
        # part 2 of ALFRED's tryptic
        self.runApp02Cmd = "python.exe App02.py &"

        # set App 03
        # app that runs GAN
        # part 3 of ALFRED's tryptic
        self.runApp03Cmd = "python.exe App03.py &"

        # run all apps
        self.runApps()

        # frames
        runButton = Button(self.window, text="RUN", command=self.runApps)
        killButton = Button(self.window, text="STOP", command=self.killApps)
        runApp01Button = Button(self.window, text="RUN APP01", command=self.runApp01)
        runApp02Button = Button(self.window, text="RUN APP02", command=self.runApp02)
        runApp03Button = Button(self.window, text="RUN APP03", command=self.runApp03)
        killApp01Button = Button(self.window, text="KILL APP01", command=self.killApp01)
        killApp02Button = Button(self.window, text="KILL APP02", command=self.killApp02)
        killApp03Button = Button(self.window, text="KILL APP03", command=self.killApp03)
        runButton.pack()
        killButton.pack()
        runApp01Button.pack()
        killApp01Button.pack()
        runApp02Button.pack()
        killApp02Button.pack()
        runApp03Button.pack()
        killApp03Button.pack()

        # run main loop
        self.window.protocol("WM_DELETE_WINDOW", self.killMainApp)
        self.window.mainloop()

    def runApps(self):
        self.app01 = subprocess.Popen(self.runApp01Cmd)
        self.app02 = subprocess.Popen(self.runApp02Cmd)
        self.app03 = subprocess.Popen(self.runApp03Cmd)

    def runApp01(self):
        # kill app if already running
        if self.app01.poll() == None:
            print("App01 already running.")
            self.killApp01()
        # run app
        self.app01 = subprocess.Popen(self.runApp01Cmd)

    def runApp02(self):
        # kill app if already running
        if self.app02.poll() == None:
            print("App02 already running.")
            self.killApp02()
        # run app
        self.app02 = subprocess.Popen(self.runApp02Cmd)

    def runApp03(self):
        # kill app if already running
        if self.app03.poll() == None:
            print("App03 already running.")
            self.killApp03()
        # run app
        self.app03 = subprocess.Popen(self.runApp03Cmd)

    def killApp01(self):
        print("Killing App01.")
        self.app01.kill()

    def killApp02(self):
        print("Killing App02.")
        self.app02.kill()

    def killApp03(self):
        print("Killing App03.")
        self.app03.kill()

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
