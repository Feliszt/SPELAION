from IPython import display
import numpy as np
from scipy.stats import truncnorm
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from numpy import linalg as LA

from tkinter import *
from PIL import Image, ImageTk
import time
import random
import math

# set sizes
screenW = 1920
screenH = 1080
appW = 800
appH = 512
outputSz = 512

class App:
    def __init__(self, window):
        # window stuff
        self.window = window
        self.window.geometry(str(appW) + "x" + str(appH) + "+" + str(math.floor(screenW * 1.5 - appW * 0.5)) + "+" + str(math.floor(screenH * 0.5 - appH * 0.5)))

        # frames
        self.canvasGAN = Canvas(self.window, width = outputSz, height = outputSz, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasGAN.pack(side = LEFT)

        # network stuff
        self.GAN = Network("https://tfhub.dev/deepmind/biggan-256/2", 0.8)

        # widgets
        self.seedSlider = Scale(self.window, from_=0, to=self.GAN.latent_size, length = 150, orient=HORIZONTAL)
        self.classASlider = Scale(self.window, from_=0, to=1, resolution = 0.01, length = 150, orient=HORIZONTAL)
        self.classBSlider = Scale(self.window, from_=0, to=1, resolution = 0.01, length = 150, orient=HORIZONTAL)
        self.classCSlider = Scale(self.window, from_=0, to=1, resolution = 0.01, length = 150, orient=HORIZONTAL)
        self.seedSlider.pack()
        self.classASlider.pack()
        self.classBSlider.pack()
        self.classCSlider.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        # generate image
        img = self.GAN.generate(self.one_hot(), self.seedSlider.get())

        # display image
        img = Image.fromarray(img).resize((outputSz, outputSz), Image.BICUBIC)
        self.canvasGAN.delete("all")
        self.canvasGAN.img = ImageTk.PhotoImage(image=img)
        self.canvasGAN.create_image(0, 0, anchor=NW, image=self.canvasGAN.img)

        # re update
        self.window.after(self.delay, self.update)

    #helper functions to generate the encoding
    def one_hot(self):
        output = np.zeros((1, self.GAN.vocab_size), dtype=np.float32)
        output[np.arange(1), 760] = self.classASlider.get()
        output[np.arange(1), 417] = self.classBSlider.get()
        output[np.arange(1), 309] = self.classCSlider.get()
        #output = self.softmax(output)
        return output

    # softmax function
    def softmax(self, Z):
        Z = [np.exp(z) for z in Z]
        S = np.sum(Z)
        Z /= S
        return Z

class Network:
    def __init__(self, module_path, ratio_GPU):
        tf.compat.v1.reset_default_graph()
        self.module = hub.Module(module_path)
        self.inputs = {k: tf.placeholder(v.dtype, v.get_shape().as_list(), k) for k, v in self.module.get_input_info_dict().items()}
        self.output = self. module(self.inputs)
        self.vocab_size = self.inputs['y'].get_shape().as_list()[1]
        self.latent_size = self.inputs['z'].get_shape().as_list()[1]
        self.trunc = 0.4
        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = ratio_GPU
        self.sess = tf.Session(config=config)
        self.sess.run(tf.global_variables_initializer())

    #
    def generate(self, y, seed):
        # get z-tensor from seed
        z = truncnorm.rvs(-2, 2, size=(1, self.latent_size), random_state = np.random.RandomState(seed)) * self.trunc

        # run session
        feed_dict = {self.inputs['z']: z, self.inputs['y']:y, self.inputs['truncation']: self.trunc}
        im = self.sess.run(self.output, feed_dict=feed_dict)

        # postprocess the image
        im = np.clip(((im + 1) / 2.0) * 256, 0, 255)
        im = np.uint8(im)
        im = im.squeeze()
        return im

# Create a window and pass it to the Application object
App(Tk())
