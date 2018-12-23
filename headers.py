import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import math
from scipy.stats import multivariate_normal
import sys
import os
import csv
from skimage.transform import rescale, resize

# SKIN KERNEL
# Tuples mean, covariance, weight
gaussian_skin_model= {1:((73.53, 29.94, 17.76),(765.40, 121.44, 112.80), 0.0294),
                      2:((249.71, 233.94, 217.49), (39.94, 154.44, 396.05), 0.0331),
                      3:((161.68, 116.25, 96.95), (291.03, 60.48, 162.85), 0.0654),
                      4:((186.07, 136.62, 114.40), (274.95, 64.60, 198.27), 0.0756),
                      5:((189.26, 98.37, 51.18), (633.18, 222.40, 250.69), 0.0554),
                      6:((247.00, 152.20, 90.84), (65.23, 691.53, 609.92), 0.0314),
                      7:((150.10, 72.66, 37.76), (408.63, 200.77, 257.57), 0.0454),
                      8:((206.85, 171.09, 156.34), (530.08, 155.08, 572.79), 0.0469),
                      9:((212.78, 152.82, 120.04), (160.57, 84.52, 243.90), 0.0956),
                      10:((234.87, 175.43, 138.94), (163.80, 121.57, 279.22), 0.0763),
                      11:((151.19, 97.74, 74.59), (425.40, 73.56, 175.11), 0.1100),
                      12:((120.52, 77.55, 59.82), (330.45, 70.34, 151.82), 0.0676),
                      13:((192.20, 119.62, 82.32), (152.76, 92.14, 259.15), 0.0755),
                      14:((214.29, 136.08, 87.24), (204.90, 140.17, 270.19), 0.0500),
                      15:((99.57, 54.33, 38.06), (448.13, 90.18, 151.29), 0.0667),
                      16:((238.88, 203.08, 176.91), (178.38, 156.27, 404.99), 0.0749)
                      }


w_i_skin= np.array([0.0294, 0.0331, 0.0654, 0.0756,
                    0.0554, 0.0314, 0.0454, 0.0469,
                    0.0956, 0.0763, 0.11, 0.0676,
                    0.0755, 0.05, 0.0667, 0.0749])

mean_skin= np.array([(73.53, 29.94, 17.76),(249.71, 233.94, 217.49),
                     (161.68, 116.25, 96.95), (186.07, 136.62, 114.4),
                     (189.26, 98.37, 51.18), (247.0, 152.2, 90.84),
                     (150.1, 72.66, 37.76), (206.85, 171.09, 156.34),
                     (212.78, 152.82, 120.04), (234.87, 175.43, 138.94),
                     (151.19, 97.74, 74.59),(120.52, 77.55, 59.82),
                     (192.2, 119.62, 82.32),(214.29, 136.08, 87.24),
                     (99.57, 54.33, 38.06), (238.88, 203.08, 176.91)])

cov_skin_1= np.array([(765.4, 121.44, 112.8), (39.94, 154.44, 396.05), (291.03, 60.48, 162.85),
                      (274.95, 64.6, 198.27), (633.18, 222.4, 250.69), (65.23, 691.53, 609.92),
                      (408.63, 200.77, 257.57), (530.08, 155.08, 572.79), (160.57, 84.52, 243.9),
                      (163.8, 121.57, 279.22), (425.4, 73.56, 175.11), (330.45, 70.34, 151.82),
                      (152.76, 92.14, 259.15), (204.9, 140.17, 270.19), (448.13, 90.18, 151.29),
                      (178.38, 156.27, 404.99)])

cov_skin=np.array([np.array([[765.4 , 0., 0.],
       [0., 121.44, 0.],
       [0., 0., 112.8 ]]),np.array([[ 39.94, 0., 0.],
       [0., 154.44, 0.],
       [0., 0., 396.05]]),np.array([[291.03, 0., 0.],
       [0., 60.48, 0.],
       [0., 0., 162.85]]),np.array([[274.95, 0., 0.],
       [0., 64.6 , 0.],
       [0., 0., 198.27]]),np.array([[633.18, 0., 0.],
       [0., 222.4 , 0.],
       [0., 0., 250.69]]),np.array([[ 65.23, 0., 0.],
       [0., 691.53, 0.],
       [0., 0., 609.92]]),np.array([[408.63, 0., 0.],
       [0., 200.77, 0.],
       [0., 0., 257.57]]),np.array([[530.08, 0., 0.],
       [0., 155.08, 0.],
       [0., 0., 572.79]]),np.array([[160.57, 0., 0.],
       [0., 84.52, 0.],
       [0., 0., 243.9 ]]),np.array([[163.8 , 0., 0.],
       [0., 121.57, 0.],
       [0., 0., 279.22]]),np.array([[425.4 , 0., 0.],
       [0., 73.56, 0.],
       [0., 0., 175.11]]),np.array([[330.45, 0., 0.],
       [0., 70.34, 0.],
       [0., 0., 151.82]]),np.array([[152.76, 0., 0.],
       [0., 92.14, 0.],
       [0., 0., 259.15]]),np.array([[204.9 , 0., 0.],
       [0., 140.17, 0.],
       [0., 0., 270.19]]),np.array([[448.13, 0., 0.],
       [0., 90.18, 0.],
       [0., 0., 151.29]]),np.array([[178.38, 0., 0.],
       [0., 156.27, 0.],
       [0., 0., 404.99]])])



# Non skin KERNEL
gaussian_non_skin_model= {1:((254.37, 254.41, 253.82), (2.77, 2.81, 5.46), 0.0637),
                          2:((9.39, 8.09, 8.52), (46.84, 33.59, 32.48), 0.0516),
                          3:((96.57, 96.95, 91.53), (280.69, 156.79, 436.58), 0.0864),
                          4:((160.44, 162.49, 159.06), (355.98, 115.89, 591.24), 0.0636),
                          5:((74.98, 63.23, 46.33), (414.84, 245.95, 361.27), 0.0747),
                          6:((121.83, 60.88, 18.31), (2502.24, 1383.53, 237.18), 0.0365),
                          7:((202.18, 154.88, 91.04), (957.42, 1766.94, 1582.52), 0.0349),
                          8:((193.06, 201.93, 206.55), (562.88, 190.23, 447.28), 0.0649),
                          9:((51.88, 57.14, 61.55), (344.11, 191.77, 433.40), 0.0656),
                          10:((30.88, 26.84, 25.32), (222.07, 118.65, 182.41), 0.1189),
                          11:((44.97, 85.96, 131.95), (651.32, 840.52, 963.67), 0.0362),
                          12:((236.02, 236.27, 230.70), (225.03, 117.29, 331.95), 0.0849),
                          13:((207.86, 191.20, 164.12), (494.04, 237.69, 533.52), 0.0368),
                          14:((99.83, 148.11, 188.17), (955.88, 654.95, 916.70), 0.0389),
                          15:((135.06, 131.92, 123.10), (350.35, 130.30, 388.43), 0.0943),
                          16:((135.96, 103.89, 66.88), (806.44, 642.20, 350.36), 0.0477)
                          }

mean_non_skin= np.array([(254.37, 254.41, 253.82), (9.39, 8.09, 8.52),
                         (96.57, 96.95, 91.53), (160.44, 162.49, 159.06),
                         (74.98, 63.23, 46.33), (121.83, 60.88, 18.31),
                         (202.18, 154.88, 91.04), (193.06, 201.93, 206.55),
                         (51.88, 57.14, 61.55), (30.88, 26.84, 25.32),
                         (44.97, 85.96, 131.95), (236.02, 236.27, 230.7),
                         (207.86, 191.2, 164.12), (99.83, 148.11, 188.17),
                         (135.06, 131.92, 123.1), (135.96, 103.89, 66.88)])

cov_non_skin= np.array([np.array([[2.77, 0., 0.],
       [0., 2.81, 0.],
       [0., 0., 5.46]]),np.array([[46.84, 0., 0.],
       [ 0., 33.59, 0.],
       [ 0., 0., 32.48]]),np.array([[280.69, 0., 0.],
       [0., 156.79, 0.],
       [0., 0., 436.58]]),np.array([[355.98, 0., 0.],
       [0., 115.89, 0.],
       [0., 0., 591.24]]),np.array([[414.84, 0., 0.],
       [0., 245.95, 0.],
       [0., 0., 361.27]]),np.array([[2502.24, 0., 0.],
       [ 0., 1383.53, 0.],
       [ 0., 0., 237.18]]),np.array([[ 957.42, 0., 0.],
       [ 0., 1766.94, 0.],
       [ 0., 0., 1582.52]]),np.array([[562.88, 0., 0.],
       [0., 190.23, 0.],
       [0., 0., 447.28]]),np.array([[344.11, 0., 0.],
       [0., 191.77, 0.],
       [0., 0., 433.4 ]]),np.array([[222.07, 0., 0.],
       [0., 118.65, 0.],
       [0., 0., 182.41]]),np.array([[651.32, 0., 0.],
       [0., 840.52, 0.],
       [0., 0., 963.67]]),np.array([[225.03, 0., 0.],
       [0., 117.29, 0.],
       [0., 0., 331.95]]),np.array([[494.04, 0., 0.],
       [0., 237.69, 0.],
       [0., 0., 533.52]]),np.array([[955.88, 0., 0.],
       [0., 654.95, 0.],
       [0., 0., 916.7 ]]),np.array([[350.35, 0., 0.],
       [0., 130.3 , 0.],
       [0., 0., 388.43]]),np.array([[806.44, 0., 0.],
       [0., 642.2 , 0.],
       [0., 0., 350.36]])])

cov_non_skin_1= np.array([(2.77, 2.81, 5.46), (46.84, 33.59, 32.48), (280.69, 156.79, 436.58),
                         (355.98, 115.89, 591.24), (414.84, 245.95, 361.27), (2502.24, 1383.53, 237.18),
                         (957.42, 1766.94, 1582.52), (562.88, 190.23, 447.28), (344.11, 191.77, 433.4),
                         (222.07, 118.65, 182.41), (651.32, 840.52, 963.67), (225.03, 117.29, 331.95),
                         (494.04, 237.69, 533.52), (955.88, 654.95, 916.7), (350.35, 130.3, 388.43),
                         (806.44, 642.2, 350.36)])

w_i_non_skin= np.array([0.0637, 0.0516, 0.0864, 0.0636,
                        0.0747, 0.0365, 0.0349, 0.0649,
                        0.0656, 0.1189, 0.0362, 0.0849,
                        0.0368, 0.0389, 0.0943, 0.0477])

