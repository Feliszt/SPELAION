# --------------------------------------------------------
#   APP03 of Collectif TOAST's ALFRED installation
#   This app runs a GAN and displays the result
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from tkinter import *
# video / images
import cv2
import PIL.Image, PIL.ImageTk
# OSC Server
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
# TF
import tensorflow as tf
import tensorflow_hub as hub
import threading
# GAN
from scipy.stats import truncnorm
import numpy as np
from numpy import linalg as LA
# misc
import random
import math
import time
import sys
import json

# App 03
class App:
    def __init__(self, _window, _config):
        # window stuffx
        self.window = _window
        self.window.title("APP03 - GAN")
        self.window.overrideredirect(True)
        self.appW = int(_config["appW"] * 1 / 3)
        self.appH = _config["appH"]
        self.offX = _config["offX"] + int(_config["appW"] * 2 / 3)
        self.offY = _config["offY"]
        self.window.geometry("{}x{}+{}+{}".format(self.appW, self.appH, self.offX, self.offY))
        self.frameCount = 0
        self.prevTime = 0
        self.fps = 0

        # OSC server
        self.OSCAddr = _config["OSC_addr"]
        self.OSCPortApp03 = _config["OSC_port_App03"]

        # Set dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/labels", self.getLabels)

        # Launch OSC Server
        self.server = osc_server.ThreadingOSCUDPServer((self.OSCAddr, self.OSCPortApp03), self.dispatcher)
        self.serverThread = threading.Thread(target = self.server.serve_forever)
        self.serverThread.start()

        # GAN stuff
        self.frameNumber = _config["frameMemory"]
        self.topK = _config["topK"]
        self.seedChangeSpeed = _config["seedChangeSpeed"]
        self.tensorInputs = []
        self.imgToDisplay = ""
        self.imgPosX = int(self.appW * 0.5)
        self.imgPosY = int(self.appH * 0.5)
        self.changeImg = False

        # load GAN
        self.runTF = _config["runTF"]
        if(self.runTF):
            tf.compat.v1.reset_default_graph()
            self.GAN = hub.Module(_config["GANNetwork"])
            self.inputs = {k: tf.placeholder(v.dtype, v.get_shape().as_list(), k) for k, v in self.GAN.get_input_info_dict().items()}
            self.output = self.GAN(self.inputs)
            self.vocab_size = self.inputs['y'].get_shape().as_list()[1]
            self.latent_size = self.inputs['z'].get_shape().as_list()[1]
            self.trunc = 0.4

            # init session
            classifierConfig = tf.ConfigProto()
            classifierConfig.gpu_options.per_process_gpu_memory_fraction = _config["GANGPURatio"]
            self.sess = tf.Session(config=classifierConfig)
            self.sess.run(tf.global_variables_initializer())

            # load labels
            self.labels = self.getLabelsFromFile(_config["labelsFile"])

            # init seed
            self.seed = random.random() * self.latent_size
            self.targetSeed = self.seed
            print("[APP01] seed = {}".format(self.seed))

        # frames
        self.canvasGAN = Canvas(self.window, width = self.appW, height = self.appH, bd=0, highlightthickness=0, relief='ridge', bg="black")
        self.canvasGAN.pack(side = LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        # compute fps
        currTime = time.time()
        deltaTime = currTime - self.prevTime
        self.fps = int(1 / deltaTime)

        # if we allow TF
        if(self.runTF):
            # update tensorInputs
            if len(self.tensorInputs) > self.frameNumber * self.topK:
                self.tensorInputs = self.tensorInputs[-self.frameNumber*self.topK:]

            # create tensor from inputs and normalize it
            tensor = self.createTensor(self.tensorInputs)

            # change seed
            if abs(self.seed - self.targetSeed) < 0.01 :
                self.targetSeed = random.uniform(max(0, self.seed - 20), min(self.seed + 20, self.latent_size))
                #print("[App03] Change seed to : {}".format(self.targetSeed))

            # update seed
            self.seed *= self.seedChangeSpeed
            self.seed += (1-self.seedChangeSpeed) * self.targetSeed
            #print("[App03] Seed : {}\tTarget : {}".format(self.seed, self.targetSeed))

            # create readable list for debugging
            tensorReadable = tensor[tensor>0.0]
            indexes = np.where(tensor > 0.0)[1]
            tensorReadable = list(zip([self.labels[i] for i in indexes], tensorReadable))

            # generate
            img = self.generate(tensor, self.seed)

            # update image
            img = PIL.Image.fromarray(img).resize((1080, 1080), PIL.Image.BICUBIC)
            self.imgToDisplay = PIL.ImageTk.PhotoImage(image=img)
            self.canvasGAN.create_image(self.imgPosX, self.imgPosY, image = self.imgToDisplay, anchor = CENTER)

        # compute delay time for fixed FPS
        elapsedUpdate = (time.time() - currTime) * 1000
        timeToDelay = int(self.delay - elapsedUpdate)
        timeToDelay = max(1, timeToDelay)

        # show info
        #print("[APP03] delay = {}\t{} fps.".format(timeToDelay, int(self.fps)))

        # update loop
        self.frameCount += 1
        self.prevTime = currTime
        self.window.after(self.delay, self.update)

    # generate frame with GAN
    def generate(self, _y, _seed):
        #
        minSeed = int(math.floor(_seed))
        maxSeed = int(minSeed + 1)
        ratio = _seed - minSeed

        zMin = truncnorm.rvs(-2.0, 2.0, size=(1, self.latent_size), random_state = np.random.RandomState(minSeed)) * self.trunc
        zMax = truncnorm.rvs(-2.0, 2.0, size=(1, self.latent_size), random_state = np.random.RandomState(maxSeed)) * self.trunc
        z = self.interpolate_hypersphere(zMin, zMax, ratio)

        # run session
        feed_dict = {self.inputs['z']: z, self.inputs['y']:_y, self.inputs['truncation']: self.trunc}
        img = self.sess.run(self.output, feed_dict=feed_dict)

        # postprocess the image
        img = np.clip(((img + 1) / 2.0) * 256, 0, 255)
        img = np.uint8(img)
        img = img.squeeze()

        return img

    def interpolate_hypersphere(self, _v1, _v2, _ratio):
        _v1_norm = LA.norm(_v1)
        _v2_norm = LA.norm(_v2)
        _v2_normalized = _v2 * (_v1_norm / _v2_norm)

        interpolated = _v1 + (_v2_normalized - _v1) * _ratio
        interpolated_norm =  LA.norm(interpolated)
        interpolated_normalized = interpolated * (_v1_norm / interpolated_norm)

        return interpolated_normalized

    # create tensor
    def createTensor(self, _input):
        # we start with a zero tensor
        tensor = np.zeros((1, 1000), dtype=np.float32)

        # we add up each probability together
        for t in _input:
            tensor[:,t[0]] = tensor[:,t[0]] + t[1] * 0.1

        # normalize
        #tensor = tensor / max(0.1, np.amax(tensor)) * 0.8

        return tensor

    # OSC classification reception
    def getLabels(self, unused_addr, _ind, _prob):
        #print("[APP03] Receive {} @ {}".format(_ind, _prob))
        self.tensorInputs.append((_ind, _prob))

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

def main():
    # show info
    print("Running App03.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
