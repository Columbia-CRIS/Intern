"""
Driver implementation of project. Trains and evaluates models.

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from deep_learning import model
from deep_learning import util

LOG_DIR = Path(r'/home/grandpaa/workspace/PyCharm/deep_learning/logs')

RUN_NAME = 'test'
TB_DIR = LOG_DIR / 'tensorboard' / RUN_NAME
WL_DIR = LOG_DIR / 'wang_landau' / RUN_NAME


def _rand_sample(size: int, domain: tuple) -> np.ndarray:
    samp = np.random.random_sample(size) \
           * (domain[1] - domain[0]) \
           + domain[0]
    return samp


def _train_model(model: tf.keras.models.Model,
                 data: np.ndarray,
                 labels: np.ndarray,
                 epochs: int = 100,
                 val_data: np.ndarray = None,
                 val_labels: np.ndarray = None) -> 'Model':
    kwargs = {}
    if val_data is not None and val_labels is not None:
        kwargs['validation_data'] = (val_data, val_labels)

        tensorboard = tf.keras.callbacks.TensorBoard(log_dir=TB_DIR,
                                                     histogram_freq=2)
        kwargs['callbacks'] = [tensorboard]

    model.fit(data, labels,
              epochs=epochs, batch_size=32,
              **kwargs)
    return model


# Data configuration and prep
# domain = np.array([[0, 50],
#                    [0, 50],
#                    [0, 50]])
domain = (-10, 10)
#data_range = (0, 10)
data_range = (-12, 0)
peaks = [1, 5, 10]
locs = np.array([[-5],
                 [0],
                 [5]])

shekel = util.shekel(peaks, locs, negate=True)

data = np.arange(*domain, 0.005)
labels = np.array([shekel(x) for x in data])
plt.subplot(121)
plt.plot(data, labels, 'ko')
plt.subplot(122)
plt.hist(labels, bins=120, orientation='horizontal')
plt.show()

val_data = _rand_sample(len(data), domain)
val_labels = np.array([shekel(x) for x in val_data])

pred_data = _rand_sample(len(data), domain)
pred_labels = np.array([shekel(x) for x in pred_data])


if __name__ == '__main__':
    # Model training
    simple_wl = model.simple_wl_model(1)
    simple_wl.compile(optimizer=tf.train.AdamOptimizer(0.001),
                      loss='mse',
                      metrics=['mae'])

    _train_model(simple_wl, epochs=80,
                 data=data, labels=labels,
                 val_data=val_data, val_labels=val_labels
                 )
    inferred_labels = simple_wl.predict(pred_data)

    plt.plot(pred_data, pred_labels, 'ko')
    plt.plot(pred_data, inferred_labels, 'ro')
    plt.savefig(str(TB_DIR / 'final_comparison.png'))
    plt.show()

    # Wang-Landau magic
    # def energy_func(x: float) -> float:
    #     pred = simple_wl.predict(np.array([x]))
    #     return pred[0][0]

    energy_func = model.simple_classify

    freqs, hist = util.wang_landau(energy_func,
                                   domain=domain,
                                   energy_range=range(10),
                                   max_iterations=50000,
                                   check_every=200,
                                   save_every=2000,
                                   log_dir=WL_DIR,
                                   flatness=0.95,
                                   step_size=1)

    bins = list(freqs.keys())
    values = list(freqs.values())
    print(bins)
    print(values)

    # plt.subplot(141)
    # plt.title("Neural Net function")
    # plt.plot(pred_data, pred_labels, 'ko')
    # # plt.plot(pred_data, inferred_labels, 'ro')
    # plt.ylim(data_range)

    plt.subplot(121)
    plt.title("ln of energy density")
    print(bins)
    plt.hist(bins, weights=values, bins=len(bins), orientation='horizontal')
    plt.ylim(data_range)

    plt.subplot(122)
    max_val = max(values)
    norm_values = [np.e ** (value - max_val) for value in values]
    plt.title("Normalized energy densities")
    plt.hist(bins, weights=norm_values, bins=len(bins), orientation='horizontal')
    plt.ylim(data_range)

    # plt.subplot(144)
    # hist_values = list(hist.values())
    # plt.title("visited states")
    # plt.hist(bins, weights=hist_values, bins=len(bins), orientation='horizontal')
    # plt.ylim(data_range)

    # TODO: implement final save
    plt.show()
