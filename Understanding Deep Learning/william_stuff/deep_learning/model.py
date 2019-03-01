"""
Collected models to be trained and evaluated.

author: William Tong (wlt2115@columbia.edu)
date: February 12, 2019
"""

import tensorflow as tf
from tensorflow.keras import layers


def simple_wl_model(x_dims):
    """
    Concise, vanilla neural network for simple regression

    :return: Keras model
    """

    # model = tf.keras.Sequential([
    #     layers.InputLayer(input_shape=(x_dims,)),
    #     layers.Dense(128, activation='relu', input_shape=(32,)),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(64, activation='relu'),
    #     layers.Dense(1, activation='linear')
    # ])

    model = tf.keras.Sequential([
        layers.InputLayer(input_shape=(x_dims,)),
        layers.Dense(4, activation='relu'),
        layers.Dense(4, activation='relu'),
        layers.Dense(4, activation='relu'),
        layers.Dense(4, activation='relu'),

        layers.Dense(1, activation='linear')
    ])

    return model

