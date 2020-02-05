import numpy as np
from scipy.stats import truncnorm

seed = 6

randState = np.random.RandomState(seed)

#print(randState)
z = truncnorm.rvs(-2, 2, size=(1, 120), random_state =  randState) * 0.4

print(z)
