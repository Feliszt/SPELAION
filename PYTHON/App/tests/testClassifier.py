# GUI
from os import listdir
from os.path import isfile, join
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import cv2
import random
import time

# get files
imgFolder = "D:/PERSO/_IMAGES/101_ObjectCategories/bonsai/"
imgFiles = [f for f in listdir(imgFolder) if isfile(join(imgFolder, f))]

# load
tf.compat.v1.reset_default_graph()
classifier = hub.Module("https://tfhub.dev/google/imagenet/inception_v3/classification/1")
h, w = hub.get_expected_image_size(classifier)
x = tf.placeholder(tf.float32, shape=(None, h, w, 3))
y = tf.nn.softmax(classifier(x))
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.1

# set fps
fps = 60
delay = 1 / fps


with tf.Session(config=config) as sess:
    #initialize the variables
    sess.run(tf.global_variables_initializer())

    # main loop
    while True :
        #
        ind = random.randint(0, len(imgFiles) - 1)

        # get image path
        imgPath = imgFolder + imgFiles[ind]
        print(imgPath)

        # load image and process
        img = Image.open(imgPath)
        img.load()
        img = np.asarray(img, dtype="uint8")
        data = cv2.resize(img, (h, w))

        # run classification
        y_pred = sess.run(y, feed_dict={x: [data]})

        # delay
        #time.sleep(delay)
