from keras.models import *
from keras.callbacks import *
import keras.backend as K
import os
import sys
import time
import h5py
import numpy as np
from cam_utils import extract_feat_and_cam_masks
from models_utils import choose_model
from utils_datasets import read_dataset_properties, read_dataset, create_folders

# Define Paths

#dataset = 'Paris'
dataset = 'Paris'

local_search = True

top_classes = 32

batchsize = 25

model_name = 'googlenet'

dim = '1024x720'

if dataset == 'Oxford':
    # Path Dataset
    dataset_path = '/imatge/ajimenez/work/ITR/oxford/datasets_hdf5/places/' + dim +'/'
    name_h, n_chunks_h, batchsize_h, total_imgs_h = read_dataset_properties(dataset_path+'oxford_h_info.txt')
    name_v, n_chunks_v, batchsize_v, total_imgs_v = read_dataset_properties(dataset_path + 'oxford_v_info.txt')
    cams_name = '/imatge/ajimenez/work/ITR/oxford/cam_masks/' + model_name + '/' + dim + '/'
    create_folders(cams_name)
    cams_name += 'oxford'

if dataset == 'Paris':
    dataset_path = '/imatge/ajimenez/work/ITR/paris/datasets_hdf5/places/' + dim + '/'
    name_h, n_chunks_h, batchsize_h, total_imgs_h = read_dataset_properties(dataset_path + 'paris_h_info.txt')
    name_v, n_chunks_v, batchsize_v, total_imgs_v = read_dataset_properties(dataset_path + 'paris_v_info.txt')
    cams_name = '/imatge/ajimenez/work/ITR/paris/cam_masks/' + model_name+'/' + dim + '/'
    create_folders(cams_name)
    cams_name += 'paris'


print 'Dataset: ', dataset
print 'Batch size: ', batchsize
print 'Local search: ', local_search
print 'Top classes: ', top_classes

t = time.time()

# Horizontal Images

model = choose_model(model_name, 'h')

# for i in range(0, n_chunks_h):
#     print'Extracting CAMs for chunk number ', i
#     images, image_names = read_dataset(name_h + '_' + str(i) + '.h5')
#     cams_name_chunk = cams_name + '_h_' + str(i) + '.h5'
#     extract_feat_and_cam_masks(model, batchsize, images, top_classes, cams_name_chunk)

if local_search:
    if dataset == 'Oxford':
        images, image_names = read_dataset(dataset_path+'oxford_queries_h_ls.h5')
    elif dataset == 'Paris':
        images, image_names = read_dataset(dataset_path + 'paris_queries_h_ls.h5')
    cams_name_chunk = cams_name + '_queries_h_ls' + '.h5'
else:
    if dataset == 'Oxford':
        images, image_names = read_dataset(dataset_path+'oxford_queries_h.h5')
    elif dataset == 'Paris':
        images, image_names = read_dataset(dataset_path + 'paris_queries_h.h5')
    cams_name_chunk = cams_name + '_queries_h' + '.h5'

extract_feat_and_cam_masks(model, batchsize, images, top_classes, cams_name_chunk)

# Vertical Images

model = choose_model(model_name, 'v')
#
# for i in range(0, n_chunks_v):
#     print'Extracting CAMs for chunk number ', i
#     images, image_names = read_dataset(name_v + '_' + str(i) + '.h5')
#     cams_name_chunk = cams_name + '_v_' + str(i) + '.h5'
#     extract_feat_and_cam_masks(model, batchsize, images, top_classes, cams_name_chunk)

if local_search:
    if dataset == 'Oxford':
        images, image_names = read_dataset(dataset_path + 'oxford_queries_v_ls.h5')
    elif dataset == 'Paris':
        images, image_names = read_dataset(dataset_path + 'paris_queries_v_ls.h5')
    cams_name_chunk = cams_name + '_queries_v_ls' + '.h5'
else:
    if dataset == 'Oxford':
        images, image_names = read_dataset(dataset_path + 'oxford_queries_v.h5')
    elif dataset == 'Paris':
        images, image_names = read_dataset(dataset_path + 'paris_queries_v.h5')
    cams_name_chunk = cams_name + '_queries_v' + '.h5'

extract_feat_and_cam_masks(model, batchsize, images, top_classes, cams_name_chunk)

print 'Total time elapsed: ', time.time() - t