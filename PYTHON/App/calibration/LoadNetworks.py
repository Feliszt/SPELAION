# TF
import tensorflow as tf
import tensorflow_hub as hub

# network url
netUrl = "https://tfhub.dev/google/imagenet/inception_v3/classification/4"
#netUrl = "D:/PERSO/_ML/Models/INCEPTION-V3/v1"

# load network
tf.compat.v1.reset_default_graph()
net = hub.Module(netUrl)
