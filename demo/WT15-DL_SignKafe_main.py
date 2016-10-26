#!/usr/bin/env python2
# Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.

"""
Classify an image using a model archive file
"""

import os
import time

from example import classify

def classify_image(image_files, use_gpu=True):
    caffemodel = '../caffe/20151207-223900-80d9_epoch_30.0/snapshot_iter_19140.caffemodel'
    deploy_file = '../caffe/20151207-223900-80d9_epoch_30.0/deploy.prototxt'
    mean_file = '../caffe/20151207-223900-80d9_epoch_30.0/mean.binaryproto'
    labels_file = '../caffe/20151207-223900-80d9_epoch_30.0/labels.txt'

    classify(caffemodel, deploy_file, image_files,
            mean_file=mean_file, labels_file=labels_file, use_gpu=use_gpu)


if __name__ == '__main__':
    script_start_time = time.time()

    image_files = [os.path.join('../images/', f) for f in os.listdir('../images/')]

    classify_image(image_files)

    print 'Script took %s seconds.' % (time.time() - script_start_time,)
