# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 04:37:40 2022

@author: Afromullet
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import time


def calculate_samples_for_pw(pw_micro,fs):
    T = 1 / fs
    return math.ceil( pw_micro * 1e-6 / T) #Converts the pulse width to seconds since sampling period is in seconds


def example_pwm():
    freq = 10
    fs = 176000
    T = 1 / fs
    
       #Creating a pwm signal
    x = np.arange(0,1,T)
    msg = np.sin(2*np.pi * 5 *x)
    
    saw = signal.sawtooth(2 * np.pi * freq * x)
    pwm = msg < saw 
    fig,ax = plt.subplots(3)
    ax[2].plot(pwm)
    ax[1].plot(saw)
    ax[0].plot(msg)
    
    
def example_ppm_using_samples():

    freq = 10
    fs = 176000
    pw_in_micro = 50
    samples_needed_for_pw = calculate_samples_for_pw(pw_in_micro,fs)
    bit_arr = np.array([0,1,0,1,1,1,1,0,1,1,1,0,1,0,1])
    sample_bits = np.repeat(bit_arr, samples_needed_for_pw)
    
    y = np.sin(2 * np.pi * freq * sample_bits)
    
    fig,ax = plt.subplots()
    ax.plot(y)
    
def example_ppm():
    
    freq_1 = 3
    freq_2 = 7
    fs = 176000
    T = 1 / fs
    
    #Creating a pwm signal
    x = np.arange(0,2,T)
    x_split = np.array_split(x,2)
    
    msg = np.sin(2*np.pi * 5 *x)
        
    
    saw_freq_1 = np.sin(2 * np.pi * freq_1 * x_split[0])
    saw_freq_2 = signal.sawtooth(2 * np.pi * freq_2 * x_split[1])
    combined_saw = np.append(saw_freq_1,saw_freq_2)
    
    pwm = msg < combined_saw 
    
    x1 = ~pwm
    y1 = np.diff(x1)
    
    ppm=np.zeros(len(y1))
    
    k=1;
    while k<len(y1):
        if y1[k] ==1:
            ppm[k:k+50]=np.ones(50); #%pulse of width 50*0.0001=0.005 sec
            k=k+50;
        else: 
            k=k+1
    x_half_size = len(x)//2
    fig,ax = plt.subplots(4)
    ax[0].plot(x,msg)
    ax[1].plot(combined_saw)
    ax[2].plot(pwm)
    ax[3].plot(ppm)
    

def amp_shift_key():

    fs = 44100  # sampling rate
    baud = 300  # symbol rate
    Nbits = 10  # number of bits
    Ns = int(fs/baud)
    N = Nbits * Ns
    f0 = 1800
    bits = np.random.randn(Nbits,1) > 0
    np.random.seed(seed=1)
    bits = np.random.randn(Nbits,1) > 0
    M = np.tile(bits,(1,Ns))
    t = np.r_[0.0:N]/fs
    OOK = M.ravel()*np.sin(2*np.pi*f0*t)
    
    fig = plt.figure(figsize = (16,4))
    plt.plot(t,OOK)
    plt.xlabel('time [s]')    



#Using nested functions to keep things clean for now before deciding on a final method
def ppm_method_2():


    def rect(T):
        """create a centered rectangular pulse of width $T"""
        return lambda t: (-T/2 <= t) & (t < T/2)
    

    

    def pulse_train(t, at, shape):
        """create a train of pulses over $t at times $at and shape $shape"""
        return np.sum(shape(t - at[:,np.newaxis]), axis=0)

    sig = pulse_train(
        t=np.arange(100),              # time domain
        at=np.array([0, 20, 40, 80]),  # times of pulses
        shape=rect(10)                 # shape of pulse
    )

    fs = 176000
    T = 1 / fs
    sig2 = pulse_train(
        t=np.arange(0,80,T),              # time domain
        at=np.array([0, 5, 3, 80]),  # times of pulses
        shape=rect(1)                 # shape of pulse
    )
    
    fig,ax = plt.subplots()
    ax.plot(sig2)
    

ppm_method_2()