"""
Collected models to be trained and evaluated.

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import numpy as np
from scipy.special import softmax
import tensorflow as tf
from tensorflow.keras import layers

from .util import rand_sample


def simple_wl_model(x_dims) -> 'Model':
    """
    Concise, vanilla neural network for simple regression

    :return: Keras model
    """

    model = tf.keras.Sequential([
        layers.InputLayer(input_shape=(x_dims,)),
        layers.Dense(16, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(4, activation='relu'),

        layers.Dense(1, activation='linear')
    ])

    return model


def mnist_model() -> 'Model':
    """
    Simple convolutions for MNIST.
    TODO: try with convolution
    :return: compiled Keras model
    """
    model = tf.keras.Sequential([
        layers.Flatten(input_shape=(14, 14)),
        layers.Dense(128, activation=tf.nn.relu),
        layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def simple_classify(x: np.ndarray) -> int:
    W = np.array([[1, 2, -1, 5, 5, -6, 0, 6, 1, 3],
                  [0, 5, 9, -1, -2, 2, 1, 1, 1, 7],
                  [0, 0, 7, -7, -7, 5, 4, 3, 2, -3]])

    b = np.array([[-5, -2, 3, 3, 3, -5, 4, 1, 1, 3]]).transpose()

    output = np.matmul(W.transpose(), x.reshape(3, 1)) + b

    return np.argmax(softmax(output))


def make_simple_abs(n: int) -> 'function':
    data = np.arange(-1, 1, 2 / n)
    labels = np.array([abs(val) for val in data])

    def simple_abs(w: np.ndarray) -> float:
        losses = [(labels[i]
                   - (_relu(w[0] * data[i]) + _relu(w[1] * data[i])))**2
                  for i in range(len(labels))]
        total_loss = sum(losses)
        return total_loss

    return simple_abs


def _relu(x: float) -> float:
    return x * (x > 0)


def make_full_abs(n: int) -> 'function':
    data = np.arange(-1, 1, 2 / n)
    labels = np.array([abs(val) for val in data])

    def full_abs(w: np.ndarray) -> float:
        w1, w2, w3, w4, b1, b2, b3 = w

        def _predict(x: float) -> float:
            z1 = _relu(x * w1 + b1)
            z2 = _relu(x * w2 + b2)
            out = z1 * w3 + z2 * w4 + b3

            return out

        predictions = [_predict(x) for x in data]
        losses = [(labels[i] - predictions[i])**2 for i in range(len(labels))]
        total_loss = sum(losses)

        return total_loss

    return full_abs


