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

from matplotlib import pyplot


# setup environment
# ---- image formats ----
extensions = ['.bmp', '.dib', '.jpeg', '.jpg', '.jpe', '.jp2', '.png', '.webp',
              '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.tiff', '.tif']

# ---- opencv version ----
opencv = int(cv2.__version__.split('.')[0])


################################################################################

# end-points of a 1D binary array
def endpoints(array):
    end_0 = -1
    end_1 = -1
    
    if array[0] != 0:
        end_0 = 0
    if array[-1] != 0:
        end_1 = len(array)
    
    i = 0
    j = len(array) - 1
    
    while i <= j and (end_0 < 0 or end_1 < 0):
        if array[i] == 0:
            i += 1
        elif end_0 < 0:
            end_0 = i - 1
        
        if array[j] == 0:
            j -= 1
        elif end_1 < 0:
            end_1 = j + 1
    
    if end_0 < 0:
        end_0 = 0
    if end_1 < 0:
        end_1 = len(array)
    
    return (end_0, end_1)


################################################################################

# read image
def imread(path, verbose=False):
    image = None
    
    if verbose: print('loading image.................. ', end = '')
    if os.path.isfile(path):
        extn = os.path.splitext(path)[-1]
        if extn in extensions:
            image = cv2.imread(path)
            if verbose: print('done')
        else:
            if verbose: print('unsupported format')
    else:
        if verbose: print('not found')
    
    return image


################################################################################

# preprocess image
def impreprocess(image, blur_kernel_size=(3, 3), thresh=100, verbose=False):
    # convert image to grayscale
    if verbose: print('converting colorspace.......... ', end = '')
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if verbose: print('done')
    
    # apply guassian blurring to remove noise
    if verbose: print('removing noise from image...... ', end = '')
    image_blur = cv2.GaussianBlur(image_gray, blur_kernel_size, 0, 0)
    if verbose: print('done')
    
    # threshold image
    if verbose: print('thresholding image............. ', end = '')
    (_, image_th) = cv2.threshold(image_blur, thresh, 255,
                                  cv2.THRESH_BINARY_INV)
    if verbose: print('done')
    
    return [image, image_gray, image_blur, image_th]


################################################################################

# scan image along rows
def imscan_rows(image, line_space_threshold=16, verbose=False):
    # image height
    im_rows = image.shape[0]
    
    # initialize and populate accumulator
    accu_rows = numpy.sum(image, axis=1, dtype='int') // 255
    
    # find line segments along rows
    zero_samp = 0
    y_samples = []
    
    for row in range(im_rows):
        if accu_rows[row] == 0:
            zero_samp += 1
        elif zero_samp >= line_space_threshold:
            y_samples.append(row - zero_samp // 2)
            zero_samp = 0
        elif len(y_samples) == 0:
            y_samples.append(0)
            zero_samp = 0
    
    y_samples.append(im_rows - zero_samp // 2)
    
    if verbose: print('found samples along y.......... {}'.format(y_samples))
    
    return [accu_rows, y_samples]


################################################################################

# scan image along columns
def imscan_cols(image, y_samples=[], word_space_threshold=8, verbose=False):
    # image width
    im_cols = image.shape[1]
    
    # number of detected lines
    n_lines = len(y_samples) - 1
    
    # initialize and populate accumulator
    accu_cols_list = []
    
    for line in range(n_lines):
        accu_cols = numpy.sum(image[y_samples[line]:y_samples[line+1], :],
                              axis=0, dtype='int') // 255
        accu_cols_list.append(accu_cols)
    
    # find word segments along columns of each line segment
    line_index = 0
    x_samples_list = []
    
    for accu_cols in accu_cols_list:
        zero_samp = 0
        x_samples = []
        
        for col in range(im_cols):
            if accu_cols[col] == 0:
                zero_samp += 1
            elif zero_samp >= word_space_threshold:
                x_samples.append(col - zero_samp // 2)
                zero_samp = 0
            elif len(x_samples) == 0:
                x_samples.append(0)
                zero_samp = 0
        
        x_samples.append(im_cols - zero_samp // 2)
        x_samples_list.append(x_samples)
        
        if verbose:
            print('line {:2d} samples along x........ {}'
                  .format(line_index, x_samples))
            line_index += 1
    
    return [accu_cols_list, x_samples_list]


################################################################################

# draw boundaries on image
def imdraw_boundary(image, y_samples, x_samples_list,
                    color=(0, 255, 0), width=1):
    # line boundaries
    for y in y_samples:
        cv2.line(image, (0, y), (image.shape[1]-1, y), color, width)
    
    # word boundaries
    i = 0
    
    for x_samples in x_samples_list:
        for x in x_samples:
            cv2.line(image, (x, y_samples[i]), (x, y_samples[i+1]),
                     color, width)
        
        i += 1
    
    return image


################################################################################

# draw bounding boxes on image
def imdraw_bbox(image, image_th, y_samples, x_samples_list,
                color=(0, 255, 0), width=1):
    # number of detected lines
    n_lines = len(y_samples) - 1
    
    # process objects in image
    image_rois = []
    
    for line in range(n_lines):
        x_samples = x_samples_list[line]
        n_words = len(x_samples) - 1
        
        for word in range(n_words):
            row_0 = y_samples[line]
            row_1 = y_samples[line+1]
            col_0 = x_samples[word]
            col_1 = x_samples[word+1]
            
            subimage = image_th[row_0:row_1, col_0:col_1]
            
            accu_rows = numpy.sum(subimage, axis=1, dtype='int')
            accu_cols = numpy.sum(subimage, axis=0, dtype='int')
            
            (bbox_row_0, bbox_row_1) = endpoints(accu_rows)
            (bbox_col_0, bbox_col_1) = endpoints(accu_cols)
            
            image_roi = subimage[bbox_row_0:bbox_row_1, bbox_col_0:bbox_col_1]
            image_rois.append(image_roi)
            
            offset_x = x_samples[word]
            offset_y = y_samples[line]
            
            cv2.rectangle(image, (bbox_col_0+offset_x, bbox_row_0+offset_y),
                          (bbox_col_1+offset_x, bbox_row_1+offset_y),
                          color, width)
    
    return [image_rois, image]


################################################################################

# plot histogram
def plot_hist(accu_rows, accu_cols_list):
    pyplot.figure()
    pyplot.title('Horizontal Scan')
    pyplot.xlabel('Frequency')
    pyplot.ylabel('Row')
    pyplot.gca().invert_yaxis()
    pyplot.barh(range(len(accu_rows)), accu_rows)
    
    line = 0
    
    for accu_cols in accu_cols_list:
        pyplot.figure()
        pyplot.title('Vertical Scan of Line {}'.format(line))
        pyplot.xlabel('Column')
        pyplot.ylabel('Frequency')
        pyplot.bar(range(len(accu_cols)), accu_cols)
    
    pyplot.show()
    
    return


################################################################################

# scan image by histogram
def imscanH(path, boundary_color=(0, 255, 0), boundary_width=1,
            bbox_color=(255, 0, 0), bbox_width=1, plot=False, verbose=False):
    # read image
    image = imread(path, verbose=verbose)
    
    # exit if read fails
    if image is None:
        return
    
    # preprocess image
    image_th = impreprocess(image, verbose=verbose)[-1]
    
    # scan image along rows
    [accu_rows, y_samples] = imscan_rows(image_th, verbose=verbose)
    
    # scan image along columns
    [accu_cols_list, x_samples_list] = imscan_cols(image_th, y_samples,
                                                   verbose=verbose)
    
    # draw boundaries on image
    image = imdraw_boundary(image, y_samples, x_samples_list,
                            boundary_color, boundary_width)
    
    [image_rois, image] = imdraw_bbox(image, image_th,
                                      y_samples, x_samples_list,
                                      bbox_color, bbox_width)
    
    # plot histogram
    if plot:
        plot_hist(accu_rows, accu_cols_list)
    
    return [image, image_rois]


################################################################################

# scan image for contours
def imscanC(path, bbox_color=(0, 255, 0), bbox_width=1, verbose=False):
    # read image
    image = imread(path, verbose=verbose)
    
    # exit if read fails
    if image is None:
        return
    
    # preprocess image
    image_th = impreprocess(image, verbose=verbose)[-1]
    
    # find contours
    if opencv == 2:
        (contours, _) = cv2.findContours(image_th.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_NONE)
    else:
        (_, contours, _) = cv2.findContours(image_th.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_NONE)
    
    # find bounding rectangle around each contour
    bn_rects = []
    for cntr in contours:
        bn_rects.append(cv2.boundingRect(cntr))
    
    # sort bounding rectangles from left to right
    bn_rects.sort(key=lambda x: x[0])
    
    # process each bounding rectangle
    image_rois = []
    
    for rect in bn_rects:
        # attributes of bounding rectangle
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        
        # ignore tiny objects assuming them as noise
        if h <= 8:
            continue
        
        # draw bounding rectangle on image
        cv2.rectangle(image, (x, y), (x+w, y+h), bbox_color, bbox_width)
        
        # extract region of interest from thresholded image using attributes of
        # bounding rectangle
        image_roi = image_th[y:y+h, x:x+w]
        image_rois.append(image_roi)
    
    return [image, image_rois]
