import numpy as np
from scipy.stats import truncnorm

def softmax(Z):
    Z = [np.exp(z) for z in Z]
    S = np.sum(Z)
    Z /= S
    return Z

#helper functions to generate the encoding
def one_hot(index, vocab_size=1000):
    index = np.asarray(index)
    if len(index.shape) == 0:
        index = np.asarray([index])
    assert len(index.shape) == 1
    num = index.shape[0]
    #
    output = np.zeros((num, vocab_size), dtype=np.float32)
    output[np.arange(num), index] = 1

    # test
    output = np.zeros((num, vocab_size), dtype=np.float32)
    output[np.arange(num), 0] = 85
    output[np.arange(num), 1] = 0
    output = output.astype('float32')
    output = softmax(output)
    return output

# coordinate function
def get_zy(index, trunc = 1., batch_size = 1, seed = None):
    #convert the label to one hot encoding
    y = one_hot(index, vocab_size)

    #sample a batch of z-vectors
    z = truncnorm.rvs(-2, 2, size=(batch_size, latent_size), random_state = np.random.RandomState(seed)) * trunc
    return z, y

#
vocab_size = 1000
latent_size = 140
trunc = 0.4
classInd = 0
seedInd = 0
z, y = get_zy(classInd, trunc = trunc, seed = seedInd)

print(y)
