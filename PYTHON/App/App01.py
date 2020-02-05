# --------------------------------------------------------
#   APP01 of Collectif TOAST's ALFRED installation
#   This app captures what a USB cam sees and perform
#   a classification every frame.
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# video / images
import cv2
import PIL.Image, PIL.ImageTk
from skimage import transform
# OSC Client
from pythonosc import osc_message_builder
from pythonosc import udp_client
# TF
import tensorflow as tf
import tensorflow_hub as hub
import threading
# misc
import numpy as np
import time
import sys
import os
import random
import json

# App 01
class App:
    def __init__(self, _window, _config):
        # set window
        self.window = _window
        self.window.title("APP01 - Classification")
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"]
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))
        self.frameCount = 0
        self.prevTime = 0
        self.fps = 0

        # Set OSC addresses and ports
        self.OSCAddr = _config["OSC_addr"]
        self.OSCPortApp02 = _config["OSC_port_App02"]
        self.OSCPortApp03 = _config["OSC_port_App03"]

        # OSC clients
        self.OSCClientToApp02 = udp_client.SimpleUDPClient(self.OSCAddr, self.OSCPortApp02)
        self.OSCClientToApp03 = udp_client.SimpleUDPClient(self.OSCAddr, self.OSCPortApp03)

        # cam stuff
        self.camIndex = _config["camIndex"]
        self.camW = _config["camW"]
        self.camH = _config["camH"]
        self.camPosX = int(self.appW * 0.5)
        self.camPosY = int(self.appH * 0.5)
        self.cam = VideoCapture(self.camIndex, self.camW, self.camH)

        # crop stuff
        self.cropMinW = _config["cropMinW"]
        self.cropMaxW = _config["cropMaxW"]
        self.cropMinH = _config["cropMinH"]
        self.cropMaxH = _config["cropMaxH"]

        # load labels
        self.labels = self.getLabelsFromFile(_config["labelsFile"])

        # load classifier
        self.runTF = _config["runTF"]
        if(self.runTF):
            # get network data
            tf.compat.v1.reset_default_graph()
            self.classifier = hub.Module(_config["classifierNetwork"])
            self.classifierInputH, self.classifierInputW = hub.get_expected_image_size(self.classifier)
            self.classifierInput = tf.placeholder(tf.float32, shape=(None, self.classifierInputH, self.classifierInputW, 3))
            self.classifierOutput = tf.nn.softmax(self.classifier(self.classifierInput))

            # init session
            classifierConfig = tf.ConfigProto()
            classifierConfig.gpu_options.per_process_gpu_memory_fraction = _config["classifierGPURatio"]
            self.sess = tf.Session(config=classifierConfig)
            self.sess.run(tf.global_variables_initializer())
            self.topK = _config["topK"]

        # Create a canvas that can fit the above video source size
        self.canvasVIDEO = Canvas(_window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg='black')
        self.canvasVIDEO.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 50
        self.update()
        self.window.mainloop()

    def update(self):
        # compute fps
        currTime = time.time()
        deltaTime = currTime - self.prevTime
        self.fps = 1 / deltaTime

        # Get a frame from the video source
        ret, frame = self.cam.get_frame()
        if ret:
            self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvasVIDEO.create_image(self.camPosX, self.camPosY, image = self.img, anchor = CENTER)

            # Run classification neural network
            if(self.runTF):
                # perform classification
                if(threading.active_count()) <= 5:
                    t = threading.Thread(target=self.classify, args=(frame,))
                    t.start()

        # compute delay time for fixed FPS
        elapsedUpdate = (time.time() - currTime) * 1000
        timeToDelay = int(self.delay - elapsedUpdate)
        timeToDelay = max(1, timeToDelay)

        # display info
        #print("[APP01] delay = {}\t{} fps\t{} threads.".format(timeToDelay, int(self.fps), threading.active_count()))

        # update loop
        self.frameCount += 1
        self.prevTime = currTime
        self.window.after(timeToDelay, self.update)

    # perform classification
    def classify(self, _frame):
        # crop image
        frameCropped = _frame[self.cropMinH:-self.cropMaxH,self.cropMinW:-self.cropMaxW,:]

        # resize image and prepare data
        data = cv2.resize(frameCropped, (self.classifierInputH, self.classifierInputW))
        data = data / 255

        # run classification
        y_pred = self.sess.run(self.classifierOutput, feed_dict={self.classifierInput: [data]})
        y_pred = y_pred[0][1:]
        maxInd = np.argsort(y_pred)
        top1_name = self.labels[maxInd[-1]].replace(' ', '_')
        topk_index = maxInd[-self.topK:]
        topk_prob = y_pred[maxInd[-self.topK:]]

        # send result over OSC to APP02
        self.OSCClientToApp02.send_message("/changeImage", top1_name)

        # send result over OSC to APP02
        for ind, prob in zip(topk_index, topk_prob):
            msgToApp03 = osc_message_builder.OscMessageBuilder(address = '/labels')
            msgToApp03.add_arg(ind, arg_type='i')
            msgToApp03.add_arg(prob, arg_type='f')
            msgToApp03 = msgToApp03.build()
            self.OSCClientToApp03.send(msgToApp03)

    # get indexes
    def getLabelsFromFile(self, _fileName) :
        list = []
        with open(_fileName, "r") as classesFile:
            while True:
                line = classesFile.readline()
                if not line:
                    break
                line = line.strip()
                name = line.split(',')[0]
                list.append(name)
        return list

# video capture class
class VideoCapture:
    def __init__(self, _video_source, _camW, _camH):
        # Open the video source
        self.cam = cv2.VideoCapture(_video_source)
        if not self.cam.isOpened():
            raise ValueError("Unable to open video source", _video_source)
        else:
            print("[APP01] Setting up camera with input size [" + str(_camW) + "," + str(_camH) + "] successful")

        # Set video size
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, _camW)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, _camH)

        # Get video source width and height
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # get frame
    def get_frame(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.rotate(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.ROTATE_90_COUNTERCLOCKWISE))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cam.isOpened():
            self.cam.release()

def main():
    # show info
    print("Running App01.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
