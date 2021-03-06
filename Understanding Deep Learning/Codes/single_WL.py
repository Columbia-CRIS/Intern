import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import utils
import sys
import math
import threading
import random
import pickle
import matplotlib.pyplot as plt
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
g_map = {} #map from bin endpoints to densities
histogram = {} #map from bin endpoints to counts
num_bins = 10 #to check for convergence

min_energy = -6
max_energy = -0.1 #upper bound for bin - 
flatness = 0.9
check_iteration = 20
num_flat = 2
overlapping_factor = .75
#num_threads =
#we split up the energy landscape into subwindows, with adjacent subwindows overlapping. Then, we spawn m different threads for each subwindo
#These m different threads each independently run WL on their own bins and histograms, over the subwindow they're working on
#Once all the threads for a subwindow have finished an iteration, g(E) is averaged across threads
#After a certain number of monte carlo steps, randomly swap walkers i and j
#maintain a map from subwindow to random walker
bins = []
#splits energy landscape into bins
i = min_energy
while i < max_energy:
    bins.append((i, i-max_energy/num_bins))
    i -= max_energy/num_bins
    #print(i)

for t in bins:
    g_map[t] = 0
    histogram[t] = 0

#resets histogram when flat
def reset():
    for t in bins:
        histogram[t] = 0

def test_costf(x):
    return x*x

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
    g_map[endpts] = g_map[endpts] + np.log(alpha)

def update_histogram(energy):
    endpts = get_endpoints(energy)
    histogram[endpts] += 1

def flat():
    flat_count = 0
    mean_height = 0
    min_height = sys.maxsize
   
    for b in histogram:
        mean_height += histogram[b]
        min_height = min(min_height, histogram[b])

    mean_height = mean_height/(len(histogram)*1.0)

    for b in histogram:
        if histogram[b] <= .9*mean_height:
            flat_count+=1

    if mean_height*.9 > min_height and flat_count > num_flat:
        return False

    return True

def save_dict(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_dict(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#shekel with 3 local minima, using hardcoded values for C and B
def shekel(x):
    m = 3
    C = [4.0, 1.0, 8.0]
    B = [.1, .2, .2]
    f = 0
    for i in range(0, m):
        f += math.pow(math.pow((x - C[i]), 2) + B[i], -1)
    return -1*f

def wang_landau(alpha, epsilon):
    #x_i = np.random.normal(size = 784*12 + 12 + 12*num_classes + num_classes) # a random initial configuration
    #currentEnergy = cost_function(x_i)
    x_i = random.uniform(0, 2)
    currentEnergy = shekel(x_i)
    print(currentEnergy)
    iteration = 1
    
    while alpha - 1 > epsilon:
        print("Iteration: %d" % iteration)
        #x_propose = np.random.normal(size = 784*12 + 12 + 12*num_classes + num_classes)
        #proposedEnergy = cost_function(x_propose) # the energy of the proposed configuration computed
        x_propose = random.uniform(0, 2)
        proposedEnergy = shekel(x_propose)
        if proposedEnergy > max_energy or proposedEnergy < min_energy:
            continue
        print("current Energy: %f %f %f" % (x_i, currentEnergy, g_function(currentEnergy)))
        print("proposed Energy: %f %f %f" % (x_propose, proposedEnergy, g_function(proposedEnergy)))
        p_i = 1/(g_function(currentEnergy)*1.0 + .002)
        p_propose = 1/(g_function(proposedEnergy)*1.0 + .002)
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
                print("Resetting alpha to: %f" % alpha)
                reset()
    
        iteration += 1

alpha = math.e
epsilon = .1
wang_landau(alpha, epsilon)
save_dict(g_map, 'densities_shekel_new')
#d_map = load_dict('densities')
'''min_v = -1
for v in d_map:
    if min_v == -1:
        min_v = d_map[v]
        continue
    if d_map[v] < min_v:
        min_v = d_map[v]

print(min_v)
x = []
y = []
for v in d_map:
    print(v)
    print(d_map[v]/min_v)
    x.append((v[0] + v[1])/2)
    y.append(d_map[v]/min_v)
plt.scatter(x, y)
plt.xlabel('Midpoints of Energy Bins')
plt.ylabel('Densities')
plt.title('Densities of States Map')
plt.show()
i = 0
comp_map = {}
for b in bins:
    comp_map[b] = 0
while i <= 2:
    cur = shekel(i)
    for b in bins:
        if cur >= b[0] and cur < b[1]:
            comp_map[b] += 1
            break
    i += .1
for b in bins:
    print(b)
    print(comp_map[b])'''

new_x = []
new_y = []
'''for v in comp_map:
    new_x.append((v[0] + v[1])/2.0)
    new_y.append(comp_map[v])
plt.scatter(new_x, new_y)
plt.xlabel('Midpoints of Energy Bins')
plt.ylabel('Densities')
plt.title('Comparative Densities of States Map')
plt.show()'''
i = 0
while i <= 2:
    new_x.append(i)
    new_y.append(shekel(i))
    i += .005
plt.scatter(new_x, new_y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Shekel Function on Input [0, 2]")
plt.show()