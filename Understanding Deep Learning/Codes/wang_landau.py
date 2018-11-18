import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import utils
import sys
import math

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = utils.to_categorical(y_train)
y_test = utils.to_categorical(y_test)
num_classes = y_test.shape[1]

def baseline_model(w1, b1, w2, b2):
    # create model
    model = Sequential()
    l1 = Dense(12, input_dim=num_pixels, kernel_initializer='uniform', activation='relu')
    l2 = Dense(num_classes, kernel_initializer='normal', activation='softmax')
    model.add(l1)
    model.add(l2)
    l1.set_weights([w1, b1])
    l2.set_weights([w2, b2])
    model.trainable = False
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
    
#scores = model.evaluate(X_test, y_test, verbose=0)
#print("Baseline Error: %.2f%%" % (100-scores[1]*100))

#using entire dataset to approximate weight distribution
X_final = np.append(X_train, X_test, axis = 0)
y_final = np.append(y_train, y_test, axis = 0)
 
#energy is defined as cross entropy over entire training set 
g_map = {} #map from bin endpoints to densities
histogram = {} #map from bin endpoints to counts
num_bins = 100

min_energy = 0
max_energy = np.log(100) #upper bound for bin - 
#if the network predicts a probability of .01 for the correct label for every sample, then the energy will be num_samples times this amount
flatness = 0.9
check_iteration = 100
bins = []
#splits energy landscape into bins
i = min_energy
while i <= max_energy:
    bins.append((i, i+max_energy/num_bins))
    i += max_energy/num_bins

for t in bins:
    g_map[t] = 1
    histogram[t] = 0

#resets histogram when flat
def reset():
    for t in bins:
        histogram[t] = 0


def cost_function(weights):
    w1 = np.split()
    w2 = np.split()
    model = baseline_model(w1, w2)
    history_callback = model.fit(X_final, y_final, epochs=1, batch_size=X_final.shape[1])
    loss_history = history_callback.history["loss"]
    return loss_history[0]

def get_endpoints(energy):
    endpts = bins[0]
    for b in bins:
        if energy >= b[0] and energy < b[1]:
            endpts = b
            break

    return endpts

def g_function(energy):
    return g_map[get_endpoints(energy)]
    
def update_g_function(energy, alpha):
    endpts = get_endpoints(energy)
    g_map[endpts] = g_map[endpts]*alpha

def update_histogram(energy):
    if energy in histogram:
        histogram[energy] += 1
    else:
        histogram[energy] = 1

def flat():
    mean_height = 0
    min_height = sys.maxsize
   
    for b in histogram:
        mean_height += histogram[b]
        min_height = min(min_height, histogram[b])
   
    mean_height = mean_height/(len(histogram)*1.0)
   
    if mean_height*.9 > min_height:
        return false

    return true

def wang_landau(alpha, epsilon):
    x_i = np.random.normal(size = 784*12 + 12*num_classes) # a random initial configuration
    currentEnergy = cost_function(x_i)
    iteration = 1
    
    while (alpha - 1 > epsilon):
        x_propose = np.random()  
        proposedEnergy = cost_function(x_propose) # the energy of the proposed configuration computed
       
        p_i = 1/(g_function(currentEnergy)*1.0)
        p_propose = 1/(g_function(proposedEnergy)*1.0)
        p = min(1, p_propose/p_i)
        
        indicator = np.random.binomial(1, p)
        if indicator == 1:
            x_i = x_propose
            currentEnergy = proposedEnergy
        
        update_histogram(currentEnergy)
        update_g_function(currentEnergy, alpha)

        if iteration % check_iteration == 0:
            if flat():
                alpha = math.sqrt(alpha)
                reset()
    
        iteration += 1


        