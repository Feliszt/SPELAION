# GUI
import  tkinter as tk
# video and image processing
import cv2
import PIL.Image, PIL.ImageTk
# misc
import time

# set app size and screen size
screenW = 1920
appW = 1920
appH = 1080

# get misc sizes
canvasW = appW / 3
canvasCenterX = canvasW / 2
canvasCenterY = appH / 2

# set camera resolution
camW = 1280
camH = 720

class App:
    def __init__(self, window, video_source):
        # window stuffx
        self.window = window
        self.window.overrideredirect(True)
        self.window.geometry(str(appW) + "x" + str(appH) + "+" + str(screenW) + "+0")

        # frames
        self.canvasL = tk.Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasC = tk.Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="green")
        self.canvasR = tk.Canvas(self.window, width = appW / 3, height = appH, bd=0, highlightthickness=0, relief='ridge', bg="blue")
        self.canvasL.pack(side = tk.LEFT)
        self.canvasC.pack(side = tk.LEFT)
        self.canvasR.pack(side = tk.LEFT)

        # video stuff
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvasL.create_image(canvasCenterX, canvasCenterY, image = self.photo, anchor = tk.CENTER)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Set video size
        print("Setting up camera with input size [" + str(camW) + "," + str(camH) + "]")
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, camW)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camH)

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

# Create a window and pass it to the Application object
App(tk.Tk(), 1)
