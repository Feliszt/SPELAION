# --------------------------------------------------------
#   MAINAPP of Collectif TOAST's ALFRED installation
#   This app runs app01 and app02 and kills them
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from  tkinter import *
# misc
import argparse
import time
import sys
import subprocess
import time

class App:
    def __init__(self, _window, _args):
        # window stuffx
        self.window = _window
        self.window.geometry("100x100+100+100")

        # frames
        runButton = Button(self.window, text="RUN", command=self.runApps)
        killButton = Button(self.window, text="STOP", command=self.killApps)
        runButton.pack()
        killButton.pack()

        # set App 01
        # app that runs VideoCapture and Image Classification
        # part 1 and 2 of ALFRED's tryptic
        app01offX = int(_args.offx)
        app01W = int(_args.appw * 2 / 3)
        app01H = int(_args.apph)
        self.runApp01 = "python.exe App01.py {} {} {}".format(app01offX, app01W, app01H)

        # set App 02
        # app that runs GAN
        # part 3 of ALFRED's tryptic
        app02offX = int(_args.offx + _args.appw * 2 / 3)
        app02W = int(_args.appw * 1 / 3)
        app02H = int(_args.apph)
        self.runApp02 = "python.exe App02.py {} {} {} &".format(app02offX, app02W, app02H)

        # run both apps
        self.runApps()

        # run main loop
        self.window.mainloop()

    def runApps(self):
        self.app01 = subprocess.Popen(self.runApp01)
        self.app02 = subprocess.Popen(self.runApp02)

    def killApps(self):
        self.app01.kill()
        self.app02.kill()

def main():
    # parse input
    parser = argparse.ArgumentParser(description='Run ALFRED.')
    parser.add_argument('--offx', type=int, required=True)
    parser.add_argument('--appw', type=int, required=True)
    parser.add_argument('--apph', type=int, required=True)
    args = parser.parse_args()

    # run App
    App(Tk(), args)


if __name__ == "__main__":
    main()
