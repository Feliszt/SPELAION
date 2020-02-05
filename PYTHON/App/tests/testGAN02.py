from IPython import display
import numpy as np
from scipy.stats import truncnorm
from scipy.stats import norm
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
appW = 1200
appH = 512
outputSz = 512

class App:
    def __init__(self, window):
        #
        self.TF = True

        # window stuff
        self.window = window
        self.window.geometry(str(appW) + "x" + str(appH) + "+" + str(math.floor(screenW * 1.5 - appW * 0.5)) + "+" + str(math.floor(screenH * 0.5 - appH * 0.5)))

        # frames
        self.canvasGAN = Canvas(self.window, width = outputSz, height = outputSz, bd=0, highlightthickness=0, relief='ridge', bg="red")
        self.canvasGAN.pack(side = LEFT)

        # network stuff
        #self.GAN = Network("https://tfhub.dev/deepmind/biggan-256/2", 0.8)
        if(self.TF):
            self.GAN = Network("D:/PERSO/_ML/Models/BIGGAN_128/v2", 0.8)

        # widgets
        self.seedSlider = Scale(self.window, from_=0, to=5, resolution = 0.001, length = 500, orient=HORIZONTAL)
        self.seedSlider.pack()

        self.seedStrengthSlider = Scale(self.window, from_=0, to=10, resolution = 0.001, length = 500, orient=HORIZONTAL)
        self.seedStrengthSlider.pack()

        self.truncSlider = Scale(self.window, from_=0.04, to=1.0, resolution = 0.001, length = 500, orient=HORIZONTAL)
        self.truncSlider.set(0.8)
        #self.truncSlider.pack()

        self.normSlider = Scale(self.window, from_=0.5, to=5.0, resolution = 0.01, length = 500, orient=HORIZONTAL)
        self.normSlider.set(0.9)
        #self.normSlider.pack()

        self.classes = [497, 607]
        self.classSliders = []
        for c in self.classes:
            sliderTemp = Scale(self.window, from_=0, to=4.0, resolution = 0.01, length = 500, orient=HORIZONTAL)
            sliderTemp.pack()
            self.classSliders.append((sliderTemp, c))

        #
        self.x = 50

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 33    # 30 fps
        self.update()
        self.window.mainloop()

    def update(self):
        #
        delta = 0.25
        dt = 0.1
        self.x = self.x + norm.rvs(scale=self.seedStrengthSlider.get()**2*dt)
        #self.seedSlider.set(self.x)

        # generate image
        if(self.TF) :
            #
            minSeed = int(math.floor(self.seedSlider.get()))
            maxSeed = int(minSeed + 1)
            ratio = self.seedSlider.get() - minSeed

            zMin = truncnorm.rvs(-self.normSlider.get(), self.normSlider.get(), size=(1, self.GAN.latent_size), random_state = np.random.RandomState(minSeed)) * self.truncSlider.get()
            zMax = truncnorm.rvs(-self.normSlider.get(), self.normSlider.get(), size=(1, self.GAN.latent_size), random_state = np.random.RandomState(maxSeed)) * self.truncSlider.get()
            z = self.interpolate_hypersphere(zMin, zMax, ratio)

            img = self.GAN.generate(self.one_hot(), z)

            # display image
            img = Image.fromarray(img).resize((outputSz, outputSz), Image.BICUBIC)
            self.canvasGAN.delete("all")
            self.canvasGAN.img = ImageTk.PhotoImage(image=img)
            self.canvasGAN.create_image(0, 0, anchor=NW, image=self.canvasGAN.img)

        # re update
        self.window.after(self.delay, self.update)

    #helper functions to generate the encoding
    def one_hot(self):
        # start with a 0 vector
        output = np.zeros((1, self.GAN.vocab_size), dtype=np.float32)

        # populate depending on sliders
        for t in self.classSliders:
            output[np.arange(1), t[1]] = t[0].get()

        return output

    # softmax function
    def softmax(self, Z):
        Z = [np.exp(z) for z in Z]
        S = np.sum(Z)
        Z /= S
        return Z

    def interpolate_hypersphere(self, v1, v2, ratio):
        v1_norm = LA.norm(v1)
        v2_norm = LA.norm(v2)
        v2_normalized = v2 * (v1_norm / v2_norm)

        interpolated = v1 + (v2_normalized - v1) * ratio
        interpolated_norm =  LA.norm(interpolated)
        interpolated_normalized = interpolated * (v1_norm / interpolated_norm)

        return interpolated_normalized

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
    def generate(self, y, z):
        # get z-tensor from seed
        #z = truncnorm.rvs(-2, 2, size=(1, self.latent_size), random_state = np.random.RandomState(seed)) * self.trunc

        # run session
        feed_dict = {self.inputs['z']: z, self.inputs['y']:y, self.inputs['truncation']: self.trunc}

        t1 = time.time()
        im = self.sess.run(self.output, feed_dict=feed_dict)
        t2 = time.time()

        print("{}".format(t2-t1))

        # postprocess the image
        im = np.clip(((im + 1) / 2.0) * 256, 0, 255)
        im = np.uint8(im)
        im = im.squeeze()
        return im



# Create a window and pass it to the Application object
App(Tk())
