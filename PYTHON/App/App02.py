# --------------------------------------------------------
#   APP02 of Collectif TOAST's ALFRED installation
#   This app runs a GAN and displays the result
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
        # display info
        print("Launching app02")

        # window stuffx
        self.window = _window
        self.window.overrideredirect(True)
        self.window.geometry(str(_appW) + "x" + str(_appH) + "+" + str(_appOffsetW) + "+0")

        # frames
        self.canvasGAN = Canvas(self.window, width = _appW, height = _appH, bd=0, highlightthickness=0, relief='ridge', bg="blue")
        self.canvasGAN.pack(side = LEFT)

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
