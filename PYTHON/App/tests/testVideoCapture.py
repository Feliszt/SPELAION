import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, _window, _appW, _appH, _offX, _offY):
        # set window
        self.window = _window
        self.window.overrideredirect(True)
        self.window.geometry("{}x{}+{}+{}".format(_appW, _appH, _offX, _offY))
        self.appW = _appW
        self.appH = _appH

        # open video source (by default this will try to open the computer webcam)
        self.vidW = 640
        self.vidH = 480
        self.vid = VideoCapture(1, self.vidW, self.vidH)

        # Create a canvas that can fit the above video source size
        self.canvasVIDEO = tkinter.Canvas(_window, width = int(_appW * 0.5), height = _appH, bd=0, highlightthickness=0, relief='ridge', bg='red')
        self.canvasCLASS = tkinter.Canvas(_window, width = int(_appW * 0.5), height = _appH, bd=0, highlightthickness=0, relief='ridge', bg='green')
        self.canvasVIDEO.pack(side = tkinter.LEFT)
        self.canvasCLASS.pack(side = tkinter.LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvasVIDEO.create_image(self.appW * 0.25, self.appH * 0.5, image = self.photo, anchor = tkinter.CENTER)

        self.window.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, _video_source, _camW, _camH):
        # Open the video source
        self.vid = cv2.VideoCapture(_video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", _video_source)
        else:
            print("Setting up camera with input size [" + str(_camW) + "," + str(_camH) + "] successful")

        # Set video size
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

# main
def main():
    # parse arguments
    appW = 1280
    appH = 1080
    appOffsetW = 1920
    appOffsetH = 0

    # run App
    App(tkinter.Tk(), appW, appH, appOffsetW, appOffsetH)


if __name__ == "__main__":
    main()
