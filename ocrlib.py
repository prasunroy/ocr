# -*- coding: utf-8 -*-
"""
OCR back-end server application.
Created on Mon Jul 10 11:00:00 2017
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/ocr

"""


# imports
from __future__ import division
from __future__ import print_function

import cv2
import numpy
import os

import config
import mapper

from scan import imscanC
from scan import imscanH


################################################################################

# resize and pad image
def resize_and_pad_image(image):
    # image dimension
    (h, w) = image.shape
    
    # read configurations
    dst_w = config.i_shape[1]
    dst_h = config.i_shape[2]
    box_w = config.b_shape[1]
    box_h = config.b_shape[2]
    
    if w >= h:
        new_h = h * box_w // w
        
        image = cv2.resize(image, (box_w, new_h), interpolation=cv2.INTER_AREA)
        
        pad_w = (dst_w - box_w) // 2
        pad_h = (dst_h - new_h) // 2
        
        pad_l = numpy.zeros((new_h, pad_w), dtype='uint8')
        pad_r = numpy.zeros((new_h, pad_w), dtype='uint8')
        pad_t = numpy.zeros((pad_h, dst_w), dtype='uint8')
        pad_b = numpy.zeros((dst_h-new_h-pad_h, dst_w), dtype='uint8')
        
        image = numpy.hstack((pad_l, image, pad_r))
        image = numpy.vstack((pad_t, image, pad_b))
    else:
        new_w = w * box_h // h
        
        image = cv2.resize(image, (new_w, box_h), interpolation=cv2.INTER_AREA)
        
        pad_w = (dst_w - new_w) // 2
        pad_h = (dst_h - box_h) // 2
        
        pad_l = numpy.zeros((box_h, pad_w), dtype='uint8')
        pad_r = numpy.zeros((box_h, dst_w-new_w-pad_w), dtype='uint8')
        pad_t = numpy.zeros((pad_h, dst_w), dtype='uint8')
        pad_b = numpy.zeros((pad_h, dst_w), dtype='uint8')
        
        image = numpy.hstack((pad_l, image, pad_r))
        image = numpy.vstack((pad_t, image, pad_b))
    
    return image


################################################################################

# optical character recognition
def ocr(model, file, segmentation=None, engine=None, debug=False):
    # read configurations
    dst_w = config.i_shape[1]
    dst_h = config.i_shape[2]
    
    if engine == 'en-numbers':
        th_flag = False
        db_path = config.db_path_en_numbers
    elif engine == 'en-letters':
        th_flag = False
        db_path = config.db_path_en_letters
    elif engine == 'bn-numbers':
        th_flag = True
        db_path = config.db_path_bn_numbers
    elif engine == 'bn-letters':
        th_flag = True
        db_path = config.db_path_bn_letters
    elif engine == 'dv-numbers':
        th_flag = True
        db_path = config.db_path_dv_numbers
    elif engine == 'dv-letters':
        th_flag = False
        db_path = config.db_path_dv_letters
    else:
        return ['', [], []]
    
    # scan image and find regions of interest
    if segmentation == 'contour':
        [image_scan, image_rois] = imscanC(file, bbox_width=2, verbose=debug)
    elif segmentation == 'histogram':
        [image_scan, image_rois] = imscanH(file, boundary_width=2, bbox_width=2,
                                           verbose=debug)
    else:
        return ['', [], []]
    
    # process each region of interest
    prediction = []
    predprobas = []
    
    for image_roi in image_rois:
        # resize and pad image
        image_roi = resize_and_pad_image(image_roi)
        
        # perform negation to produce a binary image similar to training images
        if th_flag:
            image_roi = 255 - image_roi
        
        # make a copy of the image to save into database
        image_dump = image_roi.copy()
        
        # reshape and scale features
        image_roi = image_roi.astype('float64').reshape(1, 1, dst_h, dst_w)
        image_roi = image_roi / 255.0
        
        # predict label
        prob = model.predict(image_roi)
        pred = numpy.argmax(prob)
        prob = numpy.round(numpy.max(prob), 2)
        
        if engine == 'en-numbers':
            symb = str(pred)
        elif engine == 'en-letters':
            symb = chr(mapper.map2ascii_en_letters[pred])
        elif engine == 'bn-numbers':
            symb = mapper.map2unicode_bn_numbers[pred]
        elif engine == 'bn-letters':
            symb = mapper.map2unicode_bn_letters[pred]
        elif engine == 'dv-numbers':
            symb = mapper.map2unicode_dv_numbers[pred]
        elif engine == 'dv-letters':
            symb = mapper.map2unicode_dv_letters[pred]
        else:
            return ['', [], []]
        
        # append prediction to list
        prediction.append(str(symb))
        predprobas.append(str(prob))
        
        # save image into database
        if config.db_saving:
            dpath = os.path.join(db_path, str(pred))
            index = len(os.listdir(dpath))
            fpath = os.path.join(dpath, ''.join([str(pred), '_',
                                                 str(index), '.png']))
            
            while os.path.isfile(fpath):
                index += 1
                fpath = os.path.join(dpath, ''.join([str(pred), '_',
                                                     str(index), '.png']))
            
            cv2.imwrite(fpath, image_dump)
    
    # save image
    if debug:
        cv2.imwrite(os.path.join(config.dpath, 'scan.png'), image_scan)
    
    # prediction
    predstring = ''.join(prediction)
    
    return [predstring, prediction, predprobas]
