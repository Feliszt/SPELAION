from tkinter import *
import time

# set app size and screen size
screenW = 1920
appW = 1920
appH = 1080

class App:
    def __init__(self, window, video_source):
        # window stuff
        self.window = window
        self.window.overrideredirect(True)
        self.window.geometry(str(appW) + "x" + str(appH) + "+" + str(screenW) + "+0")

        # frames
        self.canvasL = Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasC = Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="green")
        self.canvasR = Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="blue")
        self.canvasL.pack(side = LEFT)
        self.canvasC.pack(side = LEFT)
        self.canvasR.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        self.window.after(self.delay, self.update)

# Create a window and pass it to the Application object
App(Tk(), 1)
