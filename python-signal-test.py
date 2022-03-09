# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 04:37:40 2022

@author: Afromullet
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

freq = 10
fs = 176000
T = 1 / fs

pw_in_micro = 50
pw_in_seconds =  pw_in_micro * 1e-6

samples_needed_for_pw = math.ceil(pw_in_seconds / T)

bit_arr = np.array([0,1,0,1,1,1,1,0,1,1,1,0,1,0,1])

sample_bits = np.repeat(bit_arr, samples_needed_for_pw)
y = np.sin(2 * np.pi * freq * sample_bits)

fig,ax = plt.subplots()
ax.plot(y)