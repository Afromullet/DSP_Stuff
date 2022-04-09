# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:03:34 2021

@author: Afromullet
"""
import numpy as np
import scipy.fft as sfft
import matplotlib.pyplot as plt
import scipy.constants as scipyconsts

from matplotlib import cm
import scipy.signal as sig

#Adapted from the Matlab From the code here https://github.com/MajedMH/Radar_Digital_Signal_Processing/blob/master/RadarProcessing.m

#  L Band Radar Frequency
num_targets = 5

f = pow(10,9)

# Range
R = np.array([3100, 9000 ,5500 ,7000 ,33000])
R = np.atleast_2d(R).T

# Speed
#u = 100 * ( np.random.rand(num_targets,1) - 0.5 ) 
u = np.array([40,-27,25,-42,31])
u = np.atleast_2d(u).T

# Doppler Frequency 
Fd= np.array(((2*u)/scipyconsts.c)*f)

# Slow Time Bins
M = 1024

# Fast Time Bins
L = 1000

# Slow Time PRF 
PRF=1000

# Slow Time Period
Tm = 1/PRF

# Fast Time Sampling rate 
#Fs=pow(10,6)
Fs = pow(10,6)

# Fast time period
tl= 1/Fs

# Target reflectivity
p = np.array([ 1 ,0.5, 0.25, 0.25, 0.1 ])
p = np.atleast_2d(p).T

#todo figure out why the two arrays below have to be a different shape

# Barker code for 13 chips
barker = np.array([1, 1, 1, 1 ,1, -1 ,-1 ,1 ,1, -1, 1 ,-1 ,1])
barker = np.atleast_2d(barker) #Gives is the same shape as seen in the matlab code

Ko = ((2*np.pi) / .30)

# Probigation Constant
Ko = ( (2*np.pi)/.30 )


# Filter Coefficients # conjugate
a = np.array([1, -1 ,1 ,-1 ,1 ,1 ,-1 ,-1 ,1 ,1, 1, 1, 1 ])
a = np.atleast_2d(barker)

# Unambiguous range for doppler 
Run = scipyconsts.c/(2*PRF)

# Time Delay Ranging for Monostatic Radar
to= np.round(2*R/scipyconsts.c/tl)

# Signal to clutter ratio
SCR = 100

#clutter modeling
C=  np.sqrt ( -2* np.log(1-np.random.rand(1,1000)/SCR)) * np.exp (2*np.pi*np.random.rand(1,1000)*1j)
C = C[0]

#C=  np.array([1j for i in range(1000)])

MatrixCube = np.array([])

num_targets = 5
for i in range(M):
    # The Time Dependence
    t=i*Tm
    # Copying Clutter to the Signal
    S=C.copy()
    for k in range(num_targets):      
    
        Delay = int(to[k])
        
        S[Delay:Delay+13] = S[Delay:Delay+13]  + p[k] * barker *  np.exp(1j * 2 * Ko * u[k] * t)
        
        Sfilterd = sig.lfilter(a[0],1,S) / 13
      
    #MatrixCube = np.append(MatrixCube,S.copy())
    MatrixCube = np.append(MatrixCube,Sfilterd.copy())

fig,ax = plt.subplots()
ax.plot(S)


MatrixCube = np.reshape(MatrixCube,[M,L])

FFTMatrixCube = sfft.fftshift( sfft.fft(MatrixCube,axis=0))

scaled_cube = 100 * np.log10(abs(FFTMatrixCube.T))

scaled_cube[scaled_cube == (np.inf * -1)] = 1
fig,ax = plt.subplots()
ax.imshow(scaled_cube)

L1 = np.arange(0,1024)
M1 = np.arange(-500,500)

doppler_axis,range_axis = np.meshgrid(L1, M1)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(doppler_axis,range_axis,abs(FFTMatrixCube.T),cmap=cm.coolwarm,linewidth=0, antialiased=False)
