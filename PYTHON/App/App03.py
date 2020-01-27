# --------------------------------------------------------
#   APP03 of Collectif TOAST's ALFRED installation
#   This app runs a GAN and displays the result
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# OSC Server
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
# misc
import time
import sys
import json

# App 03
class App:
    def __init__(self, _window, _config):
        # window stuffx
        self.window = _window
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"] + int(_config["appW"] * 2 / 3)
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))
        self.frameCount = 0

        # frames
        self.canvasGAN = Canvas(self.window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg="blue")
        self.canvasGAN.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 16    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):

        # update loop
        self.frameCount += 1
        self.window.after(self.delay, self.update)

def main():
    # show info
    print("Running App03.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
