"""
Driver implementation of project. Trains and evaluates models.

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from deep_learning import model
from deep_learning import util

LOG_DIR = r'/home/grandpaa/workspace/PyCharm/deep_learning/tensorboard_logs'


def _rand_sample(size):
    samp = np.random.random_sample(size) \
           * (domain[1] - domain[0]) \
           + domain[0]
    return samp


# Data configuration and prep
domain = (-10, 10)
data_range = (0, 12)
peaks = [1, 5, 10]
locs = np.array([[-5],
                 [0],
                 [5]])

shekel = util.shekel(peaks, locs)

data = np.arange(*domain, 0.01)
pred_data = _rand_sample(len(data))
val_data = _rand_sample(len(data))

labels = np.array([shekel(x) for x in data])
pred_results = np.array([shekel(x) for x in pred_data])
val_results = np.array([shekel(x) for x in val_data])

# Model training
tensorboard = tf.keras.callbacks.TensorBoard(log_dir=LOG_DIR,histogram_freq=2)

simple_wl = model.simple_wl_model(1)
simple_wl.compile(optimizer=tf.train.AdamOptimizer(0.001),
                  loss='mse',
                  metrics=['mae'])

simple_wl.fit(data, labels,
              validation_data=(val_data, val_results), callbacks=[tensorboard],
              epochs=100, batch_size=32)
results = simple_wl.predict(pred_data)

plt.plot(pred_data, results, 'ro')
plt.plot(pred_data, pred_results, 'ko')
plt.show()


# Wang-Landau magic
def energy_func(x: float) -> float:
    pred = simple_wl.predict(np.array([x]))
    return pred[0][0]


freqs, hist = util.wang_landau(energy_func,
                               domain=np.array([domain]),
                               energy_range=data_range,
                               max_iterations=10000,
                               check_every=1000,
                               update_every=500,
                               flatness=0.95,
                               resolution=10,
                               step_size=1)

# TODO: order may not be preserved in python <= 3.6
bins = list(freqs.keys())
values = list(freqs.values())
print(values)
plt.subplot(211)
plt.title("ln of energy density")
plt.hist(bins, weights=values, bins=len(bins))

plt.subplot(212)
hist_values = list(hist.values())
plt.title("visited states")
plt.hist(bins, weights=values, bins=len(bins))
plt.show()
