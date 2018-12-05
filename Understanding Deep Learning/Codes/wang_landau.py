import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import utils
import random
import sys
import math
import threading
import pickle

# fix random seed for reproducibility
'''seed = 7
np.random.seed(seed)'''

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
#g_map = {} #map from bin endpoints to densities
#histogram = {} #map from bin endpoints to counts
num_bins = 2 #to check for convergence
global_binsize = 2
num_threads = 1
min_energy = 0
start = min_energy
max_energy = 10 
check_iteration = 20
num_flat = 0
overlapping_factor = .75
#we split up the energy landscape into subwindows, with adjacent subwindows overlapping. Then, we spawn m different threads for each subwindo
#These m different threads each independently run WL on their own bins and histograms, over the subwindow they're working on
#Once all the threads for a subwindow have finished an iteration, g(E) is averaged across threads
#After a certain number of monte carlo steps, randomly swap walkers i and j
#maintain a map from subwindow to random walker
thread_map = {}
bins_to_globalmap = {}
bins_to_histogram = {}
globals_to_locals = {}
global_bins = [] #array of endpoints
alpha_init = 1.002
epsilon =  .002
alpha_map = {}
densities = {}
density_counts = {}
#locks = {}

#splits energy landscape into bins
def create_bins():
    global start
    while start + global_binsize <= max_energy:
        global_bins.append((start,start+global_binsize))
        start += (global_binsize * (1-overlapping_factor))

def init():
    create_bins()
    thread_count = 0
    for t in global_bins: 
            #lock[t] = threading.RLock()
        alpha_map[t] = alpha_init
        bins = []
        i = t[0]
        e_range = t[1] - t[0]
        while i < t[1]:
            bins.append((i, i+e_range/num_bins))
            densities[(i, i+e_range/num_bins)] = 0
            density_counts[(i, i+e_range/num_bins)] = 0
            i += e_range/(num_bins*1.0)
                
        thread_map[t] = []
        g_map = {}
        histogram = {}
        for i in range(0, num_threads):
            cur_thread = "child"+str(thread_count)
            thread_map[t].append(cur_thread)
            thread_count+=1 
            g_map[cur_thread] = {}
            histogram[cur_thread] = {}
            for b in bins:
                g_map[cur_thread][b] = 1
                histogram[cur_thread][b] = 0
                
            bins_to_globalmap[t] = g_map
            bins_to_histogram[t] = histogram
            globals_to_locals[t] = bins
    
    for t in thread_map:
        for v in thread_map[t]:
            worker = threading.Thread(target=global_wanglandau, name=v, args=(t, v))
            worker.start()
    
def global_wanglandau(subwindow, cur_thread):
    wang_landau(cur_thread, subwindow)
    for l_bin in globals_to_locals[subwindow]:
        densities[l_bin] += bins_to_globalmap[subwindow][cur_thread][l_bin]
        density_counts[l_bin] += 1

    for l_bin in densities:
        densities[l_bin] /= density_counts[l_bin] > 0 if density_counts[l_bin] > 0 else 1
    
#resets histogram when flat
def reset(histogram):
    for b in histogram:
        histogram[b] = 0

def test_costf(x):
    return x
        
def cost_function(weights):
    e1 = 784*12
    e2 = e1 + 12
    e3 = e2 + 12*num_classes
    e4 = e3 + num_classes
    spl = np.split(weights, [e1, e2, e3, e4])
    
    w1 = spl[0]
    b1 = spl[1]
    w2 = spl[2]
    b2 = spl[3]
    
    w1 = np.reshape(w1, (784, 12))
    w2 = np.reshape(w2, (12, num_classes))
    model = baseline_model(w1, b1, w2, b2)
    history_callback = model.fit(X_final, y_final, epochs=1, batch_size=X_final.shape[1])
    loss_history = history_callback.history["loss"]
    return loss_history[0]
  
def get_endpoints(energy, bins):
    endpts = bins[0]
    for b in bins:
        if energy >= b[0] and energy < b[1]:
            endpts = b
            break

    return endpts

def g_function(energy, g_map, bins):
    return g_map[get_endpoints(energy, bins)]
    
def update_g_function(energy, alpha, g_map, bins):
    endpts = get_endpoints(energy, bins)
    g_map[endpts] = g_map[endpts]*alpha

def update_histogram(energy, histogram, bins):
    endpts = get_endpoints(energy, bins)
    histogram[endpts] += 1

def flat(histogram):
    flat_count = 0
    mean_height = 0
    min_height = sys.maxsize
    for b in histogram:
        mean_height += histogram[b]
        min_height = min(min_height, histogram[b])

    mean_height = mean_height/(len(histogram)*1.0)

    for b in histogram:
        if histogram[b] <= .8*mean_height:
            flat_count+=1
    if mean_height*.8 > min_height and flat_count > num_flat:
        return False

    return True

def save_dict(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dict(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def wang_landau(cur_thread, subwindow):
    print("entering wang landau: subwindow, cur_thread - %s %f %f " % (cur_thread, subwindow[0], subwindow[1]))
    alpha = alpha_map[subwindow]
    bins = globals_to_locals[subwindow]
    g_map = bins_to_globalmap[subwindow][cur_thread]
    histogram = bins_to_histogram[subwindow][cur_thread]
    x_i = random.uniform(subwindow[0], subwindow[1])
    currentEnergy = test_costf(x_i)
    #x_i = np.random.normal(size = 784*12 + 12 + 12*num_classes + num_classes) # a random initial configuration
    #currentEnergy = cost_function(x_i)
    iteration = 1
    
    while alpha - 1 > epsilon:
        print("Iteration: %d" % iteration)
        x_propose = random.uniform(subwindow[0], subwindow[1])
        proposedEnergy = test_costf(x_propose)
        #x_propose = np.random.normal(size = 784*12 + 12 + 12*num_classes + num_classes)
        #proposedEnergy = cost_function(x_propose) # the energy of the proposed configuration computed
        print("current Energy: %f" % currentEnergy)
        print("proposed Energy: %f" % proposedEnergy)
        p_i = 1/(g_function(currentEnergy, g_map, bins)*1.0)
        p_propose = 1/(g_function(proposedEnergy, g_map, bins)*1.0)
        p = min(1, p_propose/p_i)
        
        indicator = np.random.binomial(1, p)
        if indicator == 1:
            x_i = x_propose
            currentEnergy = proposedEnergy
        
        update_histogram(currentEnergy, histogram, bins)
        update_g_function(currentEnergy, alpha, g_map, bins)

        if iteration % check_iteration == 0:
            if flat(histogram):
                alpha = math.sqrt(alpha)
                alpha_map[subwindow] = alpha
                print("Resetting alpha to: %f" % alpha)
                reset(histogram)
    
        iteration += 1
    print("Finished running WL: %s %f %f " % (cur_thread, subwindow[0], subwindow[1]))
init()
wang_landau(alpha, epsilon)
save_dict(densities, 'densities_parallel')
d_map = load_dict('densities_parallel')
for v in d_map:
    print(v)
    print(d_map[v])