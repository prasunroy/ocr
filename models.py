# -*- coding: utf-8 -*-
"""
OCR back-end server application.
Created on Mon Jul 10 11:00:00 2017
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/ocr

"""


# imports
import os

os.environ["MKL_THREADING_LAYER"] = "GNU"
os.environ["KERAS_BACKEND"] = "theano"

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend


# setup environment
backend.set_image_dim_ordering('th')


# define models
# ---- convolutional neural network architecture ----
def cnn(i_shape, n_class):
    model = Sequential()
    
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu',
                     input_shape=i_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dense(units=n_class, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model
