# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:59:22 2021

@author: Afromullet
"""

import numpy as np
import scipy.fft as sfft
import matplotlib.pyplot as plt
import scipy.constants as scipyconsts
import Plotting as plotting
from matplotlib import cm

#Implementing some matlab code in Python
#https://github.com/hortovanyi/SFND_Radar_Target_Generation_and_Detection/blob/master/radar_target_generation_and_detection.m


# Frequency of operation = 77GHz

#Radar specs
range_max = 200 #Max Range 
delta_r =1 #Range Resolution 
max_v =100 #Max Velocity in m/s

#Target info
R=150;  #Initial range
v=10;  #Velocity


#Signal parameters
Tchirp = 5.5 * (2 * range_max/scipyconsts.c) #sweep time (or chirp time) for each chirp is defined as rule by 5.5 times of round trip time for Maximum Range
Bsweep = scipyconsts.c/(2 * delta_r) #Bandwidth for the each chirp for given resolution
slope = Bsweep/Tchirp; #The slope of the chirp
fc= 10e9 #Carrier freq

#The number of chirps in one sequence. Its ideal to have 2^ value for the ease of running the FFT for Doppler Estimation. Number of doppler cells ORnumber #of sent periods % number of chirps
Nd = 128 

#The number of samples on each chirp for length of time OR number of range cells
Nr=1024;               

#Timestamp for running the displacement scenario for every sample on each chirp. total time for samples
'''
Nd*Tchirp ... How many chirps there are multiplied by how long it takes for a single chirp. Gives us the time it takes for all of the chirps
Nr*Nd tells us how many samples we need for all of the chirps

'''
t=np.linspace(0,Nd*Tchirp,Nr*Nd);

#Creating the vectors for Tx, Rx and Mix based on the total samples input.
Tx= np.zeros(len(t)); #transmitted signal
Rx= np.zeros(len(t)); #received signal
Mix = np.zeros(len(t)); #beat signal


# Similar vectors for range_covered and time delay (tau).
r_t= np.zeros(len(t));
td= np.zeros(len(t));


for i in range(len(t)):        
    
  
    #For each time stamp update the Range of the Target for constant velocity. 
    r_t[i] = R + (v*t[i]); #I think this gives us the range at every instance of time. 
    td[i] = 2 * r_t[i] / scipyconsts.c #Gives us how long it takes for a signal to return at a given range
    

   #For each time sample we need update the transmitted and received signal
 
    '''
    The equation for a chirp is: x(t) = cos(2 * pi * (mt * f) * t)
    '''    
    Tx[i] = np.cos(2*np.pi*(fc*t[i] + slope*pow(t[i],2)/2));
    Rx[i] = np.cos(2*np.pi*(fc * (t[i] -td[i]) + slope * pow(t[i] - td[i],2) /2))

    #Now by mixing the Transmit and Receive generate the beat signal
    #This is done by element wise matrix multiplication of Transmit and Receiver Signal
    Mix[i] = np.cos(2*np.pi*(2*slope*R/scipyconsts.c*t[i] + 2*fc*v/scipyconsts.c*t[i]))
    Mix[i] = Tx[i]*Rx[i]


#reshape the vector into Nr*Nd array. Nr and Nd here would also define the size of Range and Doppler FFT respectively.
'''
Creates the 'range gates', where each range gate consists of Nd number of samples
'''
Mix = np.reshape(Mix, [Nr,Nd]);


#run the FFT on the beat signal along the range bins dimension (Nr) and normalize.
Y = sfft.fft(Mix,Nr);
Y = Y / Nr;
P2 = np.abs(Y);

#Output of FFT is double sided signal, but we are interested in only one side of the spectrum. Hence we throw out half of the samples.
P1 = P2[::Nr//2]

plotting.basic_fft_plot(P1[0],'Range from First FFT') #I have no idea how this is a range...

#RANGE DOPPLER RESPONSE
#This will run a 2DFFT on the mixed signal (beat signal) output and generate a range doppler map



#Range Doppler Map Generation.

#The output of the 2D FFT is an image that has reponse in the range and
#doppler FFT bins. So, it is important to convert the axis from bin sizes
#To range and doppler based on their Max values.



#Original code has sig_fft2 = fft2(Mix,Nr,Nd)...Don't think I need dimensions as input when using scipy
sig_fft2 = sfft.fft2(Mix,[Nr,Nd]) #2D FFT using the FFT size for both dimensions.
sig_fft2 = sig_fft2[::2,] #Taking just one side of signal from Range dimension.
sig_fft2= sfft.fftshift(sig_fft2)
RDM = abs(sig_fft2)
RDM = 10*np.log10(RDM)

fig,ax = plt.subplots()
cols = 0
rows = 0
ax.imshow(RDM.transpose(),cmap='hot',origin='lower',aspect='auto')


doppler_axis = np.linspace(-100,100,Nd)
range_axis = np.linspace(-200,200,Nr//2)*((Nr//2)/400)


doppler_axis,range_axis = np.meshgrid(doppler_axis, range_axis)


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ax.plot_surface(doppler_axis,range_axis,RDM,cmap=cm.coolwarm,linewidth=0, antialiased=False)




