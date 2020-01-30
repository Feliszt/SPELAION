import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import json

class App:
    def __init__(self, _window, _config):
        # load config
        self.config = _config

        # set window
        self.window = _window
        self.window.overrideredirect(True)
        self.appW = _config["appW"]
        self.appH = _config["appH"]
        self.offX = _config["offX"]
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))
        self.frameCount = 0
        self.prevTime = 0
        self.fps = 0

        # canvas stuff
        self.canvasW = int(self.appW / 3)

        # cam stuff
        self.camIndex = _config["camIndex"]
        self.camW = _config["camW"]
        self.camH = _config["camH"]
        self.cam = VideoCapture(self.camIndex, self.camW, self.camH)

        # Canvas with full video
        self.canvasVIDEOFULL = tkinter.Canvas(_window, width = self.canvasW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg='red')
        self.canvasVIDEOFULL.pack(side = tkinter.LEFT)

        # Canvas with cropped video
        self.canvasVIDEOCROP = tkinter.Canvas(_window, width = self.canvasW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg='green')
        self.canvasVIDEOCROP.pack(side = tkinter.LEFT)

        # Add sliders
        self.cropMinW = tkinter.Scale(self.window, from_=1, to=int(self.camH * 0.5), length=self.canvasW - 50, orient=tkinter.HORIZONTAL)
        self.cropMaxW = tkinter.Scale(self.window, from_=1, to=int(self.camH * 0.5),length=self.canvasW - 50, orient=tkinter.HORIZONTAL)
        self.cropMinH = tkinter.Scale(self.window, from_=1, to=int(self.camW * 0.5) - 1, length=self.canvasW - 50, orient=tkinter.HORIZONTAL)
        self.cropMaxH = tkinter.Scale(self.window, from_=1, to=int(self.camW * 0.5) - 1, length=self.canvasW - 50, orient=tkinter.HORIZONTAL)
        self.cropMinW.pack(side = tkinter.TOP)
        self.cropMaxW.pack(side = tkinter.TOP)
        self.cropMinH.pack(side = tkinter.TOP)
        self.cropMaxH.pack(side = tkinter.TOP)

        # set slider
        self.cropMinW.set(_config["cropMinW"])
        self.cropMaxW.set(_config["cropMaxW"])
        self.cropMinH.set(_config["cropMinH"])
        self.cropMaxH.set(_config["cropMaxH"])

        # Add button
        self.saveButton = tkinter.Button(self.window, text="SAVE", command=self.saveConfig)
        self.saveButton.pack(side = tkinter.TOP)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 40
        self.update()
        self.window.mainloop()

    def update(self):
        # compute fps
        currTime = time.time()
        deltaTime = currTime - self.prevTime
        self.fps = 1 / deltaTime
        #print("[VIDEOCAPTURE] @ {}".format(self.fps))

        # Get a frame from the video source
        ret, frame = self.cam.get_frame()

        # if there is a frame
        if ret:
            # crop image
            frameCropped = frame[self.cropMinH.get():-self.cropMaxH.get(),self.cropMinW.get():-self.cropMaxW.get(),:]

            # resize image
            data = cv2.resize(frameCropped, (299, 299))
            data = data / 255

            # crop image
            self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frameCropped))
            self.canvasVIDEOFULL.create_image(int(self.canvasW * 0.5), int(self.appH * 0.5), image = self.img, anchor = tkinter.CENTER)


        # compute delay time for fixed FPS
        elapsedUpdate = (time.time() - currTime) * 1000
        timeToDelay = int(self.delay - elapsedUpdate)
        timeToDelay = timeToDelay if timeToDelay>=1 else 1

        print("[VIDEOCAPTURE] delay = {}\t@ {}".format(timeToDelay, self.fps))

        # update loop
        self.frameCount += 1
        self.prevTime = currTime
        self.window.after(timeToDelay, self.update)

    def saveConfig(self) :
        # update values
        self.config["cropMinW"] = self.cropMinW.get()
        self.config["cropMaxW"] = self.cropMaxW.get()
        self.config["cropMinH"] = self.cropMinH.get()
        self.config["cropMaxH"] = self.cropMaxH.get()

        # write them to file
        with open('../data/config.json', 'w') as outfile:
            json.dump(self.config, outfile)


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
    # show infos
    print("Running [VideoCalibration]")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('../data/config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(tkinter.Tk(), config)


if __name__ == "__main__":
    main()
