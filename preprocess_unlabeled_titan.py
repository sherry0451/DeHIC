#-*-coding:UTF-8-*-
"""
Processing unlabeled Hyperion data.

Splitting original Hyperion data into patches for subsequent network training

"""
# Authors: Jingge Xiao <jingge.xiao@gmail.com>
#
# Created on Fri Jul 28 10:21:50 2017

import numpy as np
import gdal
import os
import gc

# set batch size, which have to be same as that of labeled data.
img_size = 8

# set path of output data
npy_str = r'M:\DeepLearning\Exp\data\npy\hyper\hyper_all.npy'

# set path of input data
# each input data is a stack of bands and saved as tif format
tif_str = r'M:\DeepLearning\Exp\data\tif_scaled'

# read the list of files
fileObjectsList = []
for i in os.walk(tif_str):
    for j in i[2]:
        fileFormatStr = j[-3:]
        if fileFormatStr == 'tif':
            fileObjectsList.append(j)

# get batches from original data
list_sub_image = []
num_list = 1
for f in fileObjectsList:
    print(f)
    imagery_path = os.path.join(tif_str, f)

    # read tif files
    dataset = gdal.Open(imagery_path)
    dsmatrix = dataset.ReadAsArray(xoff=0, yoff=0, xsize=dataset.RasterXSize, ysize=dataset.RasterYSize)
    image_rows = dsmatrix.shape[1]
    image_cols = dsmatrix.shape[2]    
    image_spec = dsmatrix.shape[0]
    
    # construct pixel batches within original data margins
    for i in range(0, image_rows, img_size):
        if i >= image_rows - img_size:
            break
        for j in range(0, image_cols, img_size):
            if j >= image_cols - img_size:
                break
            break_flag = False
            sub_image = dsmatrix[:, i:i+img_size, j:j+img_size]
            
            # assign pixel values
            for p in range(0, sub_image.shape[1]):
                for q in range(0, sub_image.shape[2]):
                    
                    # batches with "NoData" pixel is not allowed
                    if np.mean(sub_image[:, p, q]) == 0.0:
                        break_flag = True
                        break
                    
                if break_flag == True:
                    break
            
            if break_flag == False:
                list_sub_image.append(sub_image)

    # collect memory
    del(dsmatrix)
    gc.collect()

# output the last list to file  
array_sub_image=np.array(list_sub_image)
np.save(npy_str, array_sub_image)