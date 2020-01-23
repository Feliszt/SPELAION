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

# create gui and canvas
master = Tk()
canvas = Canvas(master, width=1024, height=1024)
canvas.pack()

#helper functions to generate the encoding
def one_hot(index, vocab_size=1000):
    index = np.asarray(index)
    if len(index.shape) == 0:
        index = np.asarray([index])
    assert len(index.shape) == 1
    num = index.shape[0]
    output = np.zeros((num, vocab_size), dtype=np.float32)
    output[np.arange(num), index] = 1
    return output

# coordinate function
def get_zy(index, trunc = 1., batch_size = 1, seed = None):
    #convert the label to one hot encoding
    y = one_hot(index)

    #sample a batch of z-vectors
    z = truncnorm.rvs(-2, 2, size=(batch_size, latent_size), random_state = np.random.RandomState(seed)) * trunc
    return z, y

#
def generate(sess, z, y, trunc = 1.):
    feed_dict = {inputs['z']: z, inputs['y']:y, inputs['truncation']: trunc}
    im = sess.run(output, feed_dict=feed_dict)

    #postprocess the image
    im = np.clip(((im + 1) / 2.0) * 256, 0, 255)
    im = np.uint8(im)
    im = im.squeeze()
    return im

def interpolate_linear(v1, v2, num_steps):
    vectors = []
    for x in np.linspace(0.0, 1.0, num_steps):
        vectors.append(v2*x+v1*(1-x))
    return np.array(vectors)

def interpolate_hypersphere(v1, v2, num_steps):
    v1_norm = LA.norm(v1)
    v2_norm = LA.norm(v2)
    v2_normalized = v2 * (v1_norm / v2_norm)

    vectors = []
    for step in range(num_steps):
        interpolated = v1 + (v2_normalized - v1) * step / (num_steps - 1)
        interpolated_norm =  LA.norm(interpolated)
        interpolated_normalized = interpolated * (v1_norm / interpolated_norm)
        vectors.append(interpolated_normalized)
    return np.array(vectors)

#
tf.compat.v1.reset_default_graph()
model_size = "3)biggan-256" #@param ["1)biggan-128" , "2)biggan-256" , "3)biggan-512"]
#model_size = "3)biggan-128" #@param ["1)biggan-128" , "2)biggan-256" , "3)biggan-512"]
which_model = model_size.split(')')[1]
module_path = 'https://tfhub.dev/deepmind/'+which_model+'/2'
module = hub.Module(module_path)

#
inputs = {k: tf.placeholder(v.dtype, v.get_shape().as_list(), k) for k, v in module.get_input_info_dict().items()}
output = module(inputs)
print ('Inputs:\n', '\n'.join('{}: {}'.format(*kv) for kv in inputs.items()))
print ('Output:', output)

#
vocab_size = inputs['y'].get_shape().as_list()[1]
latent_size = inputs['z'].get_shape().as_list()[1]
print('Number of labels ', vocab_size)
print('The size of the latent space ', latent_size)

# session variables
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8
sess = tf.Session(config=config)
trunc = 0.4

#initialize the variables
sess.run(tf.global_variables_initializer())

classA = 100
classB = 250
seedA = 100
seedB = 100

print("Starting gui")
frameCount = 0
while True:

    num_interps = random.randint(5, 10)

    classA = classB
    #classB = random.randint(0, 999)
    classB = 450
    print("classA = " + str(classA) + "\tclassB = " + str(classB))
    seedA = seedB
    seedB = random.randint(0, 120)
    #initial interpolation
    v1, y1 = get_zy(classA, trunc = trunc, seed = seedA)
    v2, y2 = get_zy(classB, trunc = trunc, seed = seedB)

    #create interpolation for both the category and the z vector
    interps_z = interpolate_hypersphere(v1 , v2, num_interps)
    interps_y = interpolate_hypersphere(y1,  y2, num_interps)

    #create an image for each interpolation
    for i in range(0, num_interps):
        time.sleep(0.001)
        z = interps_z[i]
        y = interps_y[i]

        im = generate(sess, z, y, trunc = trunc)
        im = Image.fromarray(im).resize((1024, 1024), Image.BICUBIC)
        #images.append(im)

        canvas.delete("all")
        canvas.img = ImageTk.PhotoImage(image=im)
        canvas.create_image(0, 0, anchor=NW, image=canvas.img)

        #
        #print(frameCount)
        master.update_idletasks()
        master.update()
        frameCount = frameCount + 1
