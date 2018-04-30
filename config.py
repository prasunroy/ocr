# -*- coding: utf-8 -*-
"""
OCR back-end server application.
Created on Mon Jul 10 11:00:00 2017
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/ocr

"""


# imports
import os


# configuration variables
# ---- network ----
debug = True

_host = None
_port = None

# ---- data ----
i_shape = (1, 56, 56)
b_shape = (1, 40, 40)
n_class_en_numbers = 10
n_class_en_letters = 47
n_class_bn_numbers = 10
n_class_bn_letters = 50
n_class_dv_numbers = 10
n_class_dv_letters = 47

# ---- model ----
f_layers = 6
c_layers = 3
batch_training = 128
batch_finetune = 128
epoch_training = 100
epoch_finetune = 100

# ---- paths ----
dpath = 'data/'
mpath = 'models/'

mfile_en_numbers = os.path.join(mpath, 'en_numbers.h5')
mfile_en_letters = os.path.join(mpath, 'en_letters.h5')
mfile_bn_numbers = os.path.join(mpath, 'bn_numbers.h5')
mfile_bn_letters = os.path.join(mpath, 'bn_letters.h5')
mfile_dv_numbers = os.path.join(mpath, 'dv_numbers.h5')
mfile_dv_letters = os.path.join(mpath, 'dv_letters.h5')

tfile_en_numbers = os.path.join(mpath, 'en_numbers_ft.h5')
tfile_en_letters = os.path.join(mpath, 'en_letters_ft.h5')
tfile_bn_numbers = os.path.join(mpath, 'bn_numbers_ft.h5')
tfile_bn_letters = os.path.join(mpath, 'bn_letters_ft.h5')
tfile_dv_numbers = os.path.join(mpath, 'dv_numbers_ft.h5')
tfile_dv_letters = os.path.join(mpath, 'dv_letters_ft.h5')

db_path_en_numbers = os.path.join(dpath, 'en_numbers/')
db_path_en_letters = os.path.join(dpath, 'en_letters/')
db_path_bn_numbers = os.path.join(dpath, 'bn_numbers/')
db_path_bn_letters = os.path.join(dpath, 'bn_letters/')
db_path_dv_numbers = os.path.join(dpath, 'dv_numbers/')
db_path_dv_letters = os.path.join(dpath, 'dv_letters/')

db_saving = False
db_struct = {db_path_en_numbers: n_class_en_numbers,
             db_path_en_letters: n_class_en_letters,
             db_path_bn_numbers: n_class_bn_numbers,
             db_path_bn_letters: n_class_bn_letters,
             db_path_dv_numbers: n_class_dv_numbers,
             db_path_dv_letters: n_class_dv_letters}
