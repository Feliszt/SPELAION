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
import urllib.request

# get indexes
def populateList(fileName) :
    count = 0
    list = []
    with open(fileName, "r") as classesFile:
        while True:
            count += 1
            line = classesFile.readline()
            if not line:
                break
            line = line.strip()
            #print("{}: {}".format(count, line.strip()))
            name = line.split(',')[0]
            list.append(name)
    return list

# get files
imgFolder = "D:/PERSO/_IMAGES/101_ObjectCategories/helicopter/"
imgFiles = [f for f in listdir(imgFolder) if isfile(join(imgFolder, f))]

# get namelist
nameList = populateList("D:/TOAST/SPELAION/PYTHON/App/data/classesList.txt")

# load
tf.compat.v1.reset_default_graph()
classifier = hub.Module("https://tfhub.dev/google/efficientnet/b1/classification/1")
h, w = hub.get_expected_image_size(classifier)
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
        #print(imgPath)

        #
        resp = urllib.request.urlopen("https://www.liberaldictionary.com/wp-content/uploads/2018/12/b-e-e.png")
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)[...,::-1]

        #
        x = tf.placeholder(tf.float32, shape=(None, h, w, 3))
        y = tf.nn.softmax(classifier(x))
        data = cv2.resize(img, (h, w))

        #
        y_pred = sess.run(y, feed_dict={x: [data]})
        y_pred = y_pred[0][1:]

        print(np.where(y_pred == np.max(y_pred)))

        comment = """
        # load image and process
        img = Image.open(imgPath)
        img.load()
        img = np.asarray(img, dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)[...,::-1]
        print(img)
        #img = img.astype('float32')
        #img = img / 255
        #data = cv2.resize(img, (h, w))

        if(img.shape != (h, w, 3)):
            continue

        #print("[{}]".format(imgPath))

        # run classification
        y_pred = sess.run(y, feed_dict={x: [data]})
        y_pred = y_pred[0][1:]

        #
        #y_pred_sorted = np.sort(y_pred)
        y_pred_sortedInd = np.argsort(y_pred)
        top_k = [y_pred[ind] for ind in y_pred_sortedInd[-5:]]
        top_k_names = [nameList[ind] for ind in y_pred_sortedInd[-5:]]

        #y_pred_sortedIndex = np.argsort(y_pred)
        print("{} => {}".format(imgPath, top_k_names))
        """

        #argSorted = np.argsort(y_pred_s)
        #resultNames = [nameList[ind] for ind in argSorted[-5:]]


        # delay
        #time.sleep(delay)
