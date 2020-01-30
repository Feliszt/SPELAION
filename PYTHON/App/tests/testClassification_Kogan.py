from os import listdir
from os.path import isfile, join
import random
import numpy as np
import PIL.Image
from skimage import transform
import tensorflow as tf
import tensorflow_hub as hub
import cv2

# get indexes
def getLabelsFromFile(fileName) :
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

# get file list
labels = populateList("D:/TOAST/SPELAION/PYTHON/App/data/classesList.txt")

# get files
imgFolder = "D:/PERSO/_IMAGES/101_ObjectCategories/umbrella/"
imgFiles = [f for f in listdir(imgFolder) if isfile(join(imgFolder, f))]

# load classifier
classifier = hub.Module("https://tfhub.dev/google/imagenet/inception_v3/classification/1")
h, w = hub.get_expected_image_size(classifier)
x = tf.placeholder(tf.float32, shape=(None, h, w, 3))
y = tf.nn.softmax(classifier(x))

# init session
with tf.Session().as_default() as sess:
    tf.global_variables_initializer().run()

#
while True:
    # get random ind in folder
    ind = random.randint(0, len(imgFiles) - 1)
    imgPath = imgFolder + imgFiles[ind]

    # classify image
    img = cv2.imread(imgPath)
    data = transform.resize(img, [h, w])
    y_pred = sess.run(y, feed_dict={x: [data]})
    y_pred = y_pred[0][1:]
    maxInd = np.argsort(y_pred)

    #
    print("[{}] : [{}] @ {}".format(imgPath, labels[maxInd[-1]], int(y_pred[maxInd[-1]]*100)))
