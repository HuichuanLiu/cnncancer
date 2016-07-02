#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

print('verify trained autoencoder stage1')

import os
import sys
import csv
import numpy as np
import pickle
from PIL import Image

import tensorflow as tf

import tensorflow_ae_base
from tensorflow_ae_base import *
import tensorflow_util
import myutil

exec(open('extern_params.py').read())

ss = 512
aa = 1
batch_size = 8

if(not 'qqq_trn' in locals() or nx != ss):
    dir_input = '/Users/nono/Documents/data/tissue_images/input_w512/'
    file_input = 'qqq_trn_w512_{}.npy'.format(aa)
    path_input = os.path.join(dir_input,file_input)
    qqq_trn = np.load(path_input)
   
nn,ny,nx,nl = qqq_trn.shape
print('nn ny nx nl',nn,ny,nx,nl)

batch_size = 8
iii_vld = (0,7,9,5,1,3,4,6)
print(iii_vld)
qqq_vld = qqq_trn[iii_vld,]

# extern stamp1
# bias1c.201604061609.pkl
exec(open('tensorflow_ae_stage1.py').read())
exec(open('tensorflow_ae_stage2.py').read())

tf_encode1 = get_encode1(qqq_vld)
tf_encode2 = get_encode2(tf_encode1)
tf_deconv2 = get_deconv2(tf_encode2)
tf_deconv1 = get_deconv1(tf_deconv2)

sess.run(tf.initialize_all_variables())

##
## visualize encode
##
img_org = tensorflow_util.get_image_from_qqq(qqq_vld)

qqq_encode1 = tf_encode1.eval()
qqq_encode2 = tf_encode2.eval()
qqq_deconv2 = tf_deconv2.eval()
qqq_deconv1 = tf_deconv1.eval()

img_out = tensorflow_util.get_image_from_qqq(qqq_deconv1)
img_cmp = myutil.rbind_image(img_org,img_out)
img_cmp.show()

img_enc2 = tensorflow_util.get_image_from_encode(qqq_encode2)

print('RSEM:',np.mean((qqq_deconv1 - qqq_vld)**2))