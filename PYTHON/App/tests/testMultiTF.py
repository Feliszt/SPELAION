import tensorflow as tf
import tensorflow_hub as hub


tf.compat.v1.reset_default_graph()

moduleGAN = hub.Module('https://tfhub.dev/deepmind/biggan-512/2')
classifier = hub.Module("https://tfhub.dev/google/imagenet/nasnet_large/classification/1")

print("la")
