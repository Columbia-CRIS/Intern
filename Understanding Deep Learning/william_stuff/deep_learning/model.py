"""
Collected models to be trained and evaluated.

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import numpy as np
from scipy.special import softmax
import tensorflow as tf
from tensorflow.keras import layers


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
        layers.Flatten(input_shape=(28,28)),
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

