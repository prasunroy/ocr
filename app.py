# -*- coding: utf-8 -*-
"""
OCR back-end server application.
Created on Mon Jul 10 11:00:00 2017
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/ocr

"""


# imports
from __future__ import print_function

import base64
import os
import re
import sys

from flask import Flask
from flask import render_template
from flask import request

import config

from models import cnn
from ocrlib import ocr


# setup environment
model_en_numbers = cnn(config.i_shape, config.n_class_en_numbers)
model_en_letters = cnn(config.i_shape, config.n_class_en_letters)
model_bn_numbers = cnn(config.i_shape, config.n_class_bn_numbers)
model_bn_letters = cnn(config.i_shape, config.n_class_bn_letters)
model_dv_numbers = cnn(config.i_shape, config.n_class_dv_numbers)
model_dv_letters = cnn(config.i_shape, config.n_class_dv_letters)

if os.path.isfile(config.tfile_en_numbers):
    model_en_numbers.model.load_weights(config.tfile_en_numbers)
elif os.path.isfile(config.mfile_en_numbers):
    model_en_numbers.model.load_weights(config.mfile_en_numbers)
else:
    print('[DEBUG] network weights not found for english numbers')

if os.path.isfile(config.tfile_en_letters):
    model_en_letters.model.load_weights(config.tfile_en_letters)
elif os.path.isfile(config.mfile_en_letters):
    model_en_letters.model.load_weights(config.mfile_en_letters)
else:
    print('[DEBUG] network weights not found for english letters')

if os.path.isfile(config.tfile_bn_numbers):
    model_bn_numbers.model.load_weights(config.tfile_bn_numbers)
elif os.path.isfile(config.mfile_bn_numbers):
    model_bn_numbers.model.load_weights(config.mfile_bn_numbers)
else:
    print('[DEBUG] network weights not found for bengali numbers')

if os.path.isfile(config.tfile_bn_letters):
    model_bn_letters.model.load_weights(config.tfile_bn_letters)
elif os.path.isfile(config.mfile_bn_letters):
    model_bn_letters.model.load_weights(config.mfile_bn_letters)
else:
    print('[DEBUG] network weights not found for bengali letters')

if os.path.isfile(config.tfile_dv_numbers):
    model_dv_numbers.model.load_weights(config.tfile_dv_numbers)
elif os.path.isfile(config.mfile_dv_numbers):
    model_dv_numbers.model.load_weights(config.mfile_dv_numbers)
else:
    print('[DEBUG] network weights not found for devanagari numbers')

if os.path.isfile(config.tfile_dv_letters):
    model_dv_letters.model.load_weights(config.tfile_dv_letters)
elif os.path.isfile(config.mfile_dv_letters):
    model_dv_letters.model.load_weights(config.mfile_dv_letters)
else:
    print('[DEBUG] network weights not found for devanagari letters')

if not os.path.isdir(config.dpath):
    os.makedirs(config.dpath)
if not os.path.isdir(config.mpath):
    os.makedirs(config.mpath)

for path in config.db_struct:
    if not os.path.isdir(path):
        os.makedirs(path)
    for label in range(config.db_struct[path]):
        label_path = os.path.join(path, str(label))
        if not os.path.isdir(label_path):
            os.makedirs(label_path)

dfile = os.path.join(config.dpath, 'temp.png')
vinfo = sys.version_info[0]


################################################################################

# create a flask application
app = Flask(__name__)

# define routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.values['imageBase64']
    data = re.sub('^data:image/.+;base64,', '', data)
    
    if vinfo == 2:
        data = bytes(data)
    else:
        data = bytes(data, 'utf-8')
    
    with open(dfile, 'wb') as file:
        file.write(base64.decodestring(data))
    
    segmentation = request.values['segmentationMode']
    engine = request.values['recognitionEngine']
    
    if engine == 'en-numbers':
        model = model_en_numbers
    elif engine == 'en-letters':
        model = model_en_letters
    elif engine == 'bn-numbers':
        model = model_bn_numbers
    elif engine == 'bn-letters':
        model = model_bn_letters
    elif engine == 'dv-numbers':
        model = model_dv_numbers
    elif engine == 'dv-letters':
        model = model_dv_letters
    else:
        model = None
    
    prediction = ocr(model, dfile, segmentation, engine, debug=False)[0]
    
    return prediction


################################################################################

# main
if __name__ == '__main__':
    if config._host != None and config._port == None:
        app.run(host=config._host, debug=config.debug)
    elif config._host == None and config._port != None:
        app.run(port=config._port, debug=config.debug)
    elif config._host != None and config._port != None:
        app.run(host=config._host, port=config._port, debug=config.debug)
    else:
        app.run(debug=config.debug)
