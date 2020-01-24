# --------------------------------------------------------
#   APP01 of Collectif TOAST's ALFRED installation
#   This app captures what a USB cam sees and perform
#   a classification every frame.
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# misc
import time
import sys

class App:
    def __init__(self, _window, _appOffsetW, _appW, _appH):
        # window stuffx
        self.window = _window
        self.window.overrideredirect(True)
        self.window.geometry(str(_appW) + "x" + str(_appH) + "+" + str(_appOffsetW) + "+0")

        # frames
        self.canvasL = Canvas(self.window, width = _appW / 2, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasC = Canvas(self.window, width = _appW / 2, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="green")
        self.canvasL.pack(side = LEFT)
        self.canvasC.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):

        self.window.after(self.delay, self.update)

def main():
    # parse arguments
    appOffsetW = int(sys.argv[1])
    appW = int(sys.argv[2])
    appH = int(sys.argv[3])

    # run App
    App(Tk(), appOffsetW, appW, appH)


if __name__ == "__main__":
    main()
