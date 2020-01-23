import tensorflow as tf
import sys
from tensorflow.python.platform import gfile

from tensorflow.core.protobuf import saved_model_pb2
from tensorflow.python.util import compat

folder = "D:/PERSO/_ML/Models/EFFICIENTNET-B1/"
fileName = "saved_model.pb"

with tf.Session() as sess:
    model_filename = folder + fileName
    with gfile.FastGFile(model_filename, 'rb') as f:

        data = compat.as_bytes(f.read())
        sm = saved_model_pb2.SavedModel()
        sm.ParseFromString(data)
        #print(sm)
        if 1 != len(sm.meta_graphs):
            print('More than one graph found. Not sure which to write')
            #sys.exit(1)

        #graph_def = tf.GraphDef()
        #graph_def.ParseFromString(sm.meta_graphs[0])
        g_in = tf.import_graph_def(sm.meta_graphs[0].graph_def)

        with open(folder + "out.pb", 'wb') as f:
            f.write(sess.graph.as_graph_def().SerializeToString())
