# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:54:29 2021

@author: Afromullet
"""



import PulseTrainGenerator as pulsegen
import Plotting as Plotting
import numpy as np
import itertools
import Filters as filt
import math
import random
import OscopeAnalysis as oscope
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fft as sfft




  
                
            
def plot_oscope_data():    

    filenames = oscope.read_files("oscope_data")
    samples = oscope.read_data_into_dict(filenames[6])
    print(filenames[5])
    T = oscope.get_sampling_period(samples[oscope.X])
    
    N = 2048 * 3
    yf = sfft.fft(samples[oscope.Y],n=N)
    xf = sfft.fftfreq(N, T)[:N//2]

    fig,ax = plt.subplots(nrows = 2, ncols = 1)
    ax[0].plot(samples[oscope.X],samples[oscope.Y])
    ax[1].plot(xf, 2.0/N * np.abs(yf[0:N//2]))

   


def log_amp_decay(y):
    
    val = 2 / np.log(y) 
  

    return val
    


def apply_amp_decay(samples,decay_func):
    buf_subsets = pulsegen.SampleUtil.separate_buffer(samples)
    for index,subset in enumerate(buf_subsets):
        if pulsegen.SampleUtil.is_positive_going(subset[0]):
            pos_lengths = len(subset)
            
            #Creating an array of x values for input to the amplitude decay function. Starting at 2 to prevent division by 0, since we'll be using some sort of log decay.
            #That's also why we add 2 at the end
            x_values = np.arange(2,pos_lengths + 2) 
            y_values = list(map(decay_func,x_values))
            buf_subsets[index] = np.array(y_values)
            
    return np.hstack(buf_subsets)
            
            
         

def generate_modulated_pulse_train(existing_pulse_train, rotation_rate, beamwidth_degrees, hits_per_scan):
    fs = 1 / 176400
    duration = 5
    theta = 360 * rotation_rate * existing_pulse_train[0]

    # Calculate valid indices based on rotation angle and beamwidth, considering hits per scan
    valid_indices = np.where(
        (theta % 360 >= 180 - beamwidth_degrees / 2) & (theta % 360 <= 180 + beamwidth_degrees / 2))[0]
    valid_indices = np.tile(valid_indices, hits_per_scan)

    # Create the modulated pulse train
    modulation = np.zeros_like(existing_pulse_train[1])
    modulation[valid_indices] = existing_pulse_train[1][valid_indices]

    return existing_pulse_train[0], modulation



def calc_dwell_time(bw,rot_per_min):
    
    return bw * (1 / 360 * rot_per_min) * 60


def calc_hits_per_scan(bw,rot_per_min,pri):
    
    dwell_time = bw * (1 / 360 * rot_per_min) * 60
    hits_per_scan = dwell_time * pri
    
    return hits_per_scan


def calculate_angular_positions(rotation_rate, time_array):
    angular_positions = np.degrees(2 * np.pi * rotation_rate * time_array) % 360
    return angular_positions

PULSE_WIDTH = 4e-5
fs = 176400 

T = 1/fs
seconds = 5


beamwidth_degrees = 30  # Beamwidth in degrees
rotation_rate = 1.0 



pri = 500
train_class = pulsegen.PeriodicTrain(pri,PULSE_WIDTH)
train_x,train_y = train_class.get_timed_stable_train(fs,seconds)
train_x2,train_y2 = train_class.get_timed_stable_train(fs,seconds)


t = np.arange(0,seconds,1/fs)
angle_positions = calculate_angular_positions(rotation_rate, t)



for i,angle in enumerate(angle_positions):
    
    
    if angle > beamwidth_degrees:
        train_y2[i] = -1
    
   
pulsegen.WavFileHandler.create_wav_file("Scanning",train_y2,fs)
fig,ax = plt.subplots()

ax.set_title("Modified")
ax.plot(train_y)

fig,ax = plt.subplots()

ax.set_title("Modified")
ax.plot(train_y2)

                                                     
        

# pri = 500
# train_class = pulsegen.PeriodicTrain(pri,PULSE_WIDTH)
# train_x,train_y = train_class.get_timed_stable_train(fs,seconds)


# # Parameters for circular scan
# rotation_rate = 1.0  # Rotations per second for the scan
# beamwidth_degrees = 20.0  # Beamwidth in degrees
# # Apply modulation using Amplitude Modulation with Sinusoidal Function
# t = np.linspace(0, seconds, len(train_y), endpoint=False)
# sinusoidal_motion = np.sin(2 * np.pi * rotation_rate * t)
# modulated_pulse_train = train_y * sinusoidal_motion

# fig,ax = plt.subplots()
# ax.set_title("Original pule trian")
# ax.set_xlim(1000)
# ax.plot(train_y)


# fig,ax = plt.subplots()
# ax.set_title("Scanning motion")
# ax.plot(sinusoidal_motion)

# fig,ax = plt.subplots()
# ax.set_title("Modulated Train")
# ax.plot(modulated_pulse_train)


# pulsegen.WavFileHandler.create_wav_file("Scanning",modulated_pulse_train,fs)









