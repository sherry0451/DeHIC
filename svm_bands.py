# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 21:17:03 2017

@author: alienware
"""
from sklearn import svm
import numpy as np
import os
from sklearn.metrics import cohen_kappa_score

sub_samples_str = r"C:\DeepLearning\Exp\data\npy\ip"

x_train = np.load(os.path.join(sub_samples_str, 'training_pca_x.npy'))
y_train = np.load(os.path.join(sub_samples_str, 'training_pca_y.npy'))
x_test = np.load(os.path.join(sub_samples_str, 'validation_pca_x.npy'))
y_test = np.load(os.path.join(sub_samples_str, 'validation_pca_y.npy'))

# Train the classifier
clf_svm = svm.SVC()

clf_svm.fit(x_train, y_train)

# Predict lables based on image data
y_predict=clf_svm.predict(x_test)

kappa_value = cohen_kappa_score(y_predict, y_test)