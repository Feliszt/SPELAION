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
        self.frameNumber = 100
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

        # update tensorInputs
        if len(self.tensorInputs) > self.frameNumber * 5:
            self.tensorInputs = self.tensorInputs[-self.frameNumber*5:]

        # create tensor from inputs
        tensor = self.createTensor(self.tensorInputs)

        # if we allow TF
        if(self.runTF):
            # generate
            img = self.generate(tensor, 25)

            # update image
            img = PIL.Image.fromarray(img).resize((1080, 1080), PIL.Image.BICUBIC)
            self.imgToDisplay = PIL.ImageTk.PhotoImage(image=img)
            self.canvasGAN.create_image(self.imgPosX, self.imgPosY, image = self.imgToDisplay, anchor = CENTER)

        # compute delay time for fixed FPS
        elapsedUpdate = (time.time() - currTime) * 1000
        timeToDelay = int(self.delay - elapsedUpdate)
        timeToDelay = max(1, timeToDelay)

        # show info
        print("[APP03] delay = {}\t{} fps.".format(timeToDelay, int(self.fps)))

        # update loop
        self.frameCount += 1
        self.prevTime = currTime
        self.window.after(self.delay, self.update)

    # generate frame with GAN
    def generate(self, y, seed):
        # get z-tensor from seed
        z = truncnorm.rvs(-2, 2, size=(1, self.latent_size), random_state = np.random.RandomState(seed)) * self.trunc

        # run session
        feed_dict = {self.inputs['z']: z, self.inputs['y']:y, self.inputs['truncation']: self.trunc}
        img = self.sess.run(self.output, feed_dict=feed_dict)

        # postprocess the image
        img = np.clip(((img + 1) / 2.0) * 256, 0, 255)
        img = np.uint8(img)
        img = img.squeeze()

        return img

    # create tensor
    def createTensor(self, _input):
        # we start with a zero tensor
        tensor = np.zeros((1, 1000), dtype=np.float32)

        # we add up each probability together
        for t in _input:
            tensor[:,t[0]] = tensor[:,t[0]] + t[1]

        # normalize
        tensor = tensor / 20

        return tensor

    # OSC classification reception
    def getLabels(self, unused_addr, _ind, _prob):
        #print("[APP03] Receive {} @ {}".format(_ind, _prob))
        self.tensorInputs.append((_ind, _prob))

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
