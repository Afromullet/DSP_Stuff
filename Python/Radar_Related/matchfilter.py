# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 12:39:31 2021

@author: Afromullet
"""

#import 



import matplotlib.pyplot as plt
from scipy.constants import pi, c
from numpy import linspace, log10, zeros, exp, sqrt, finfo, conj, ones
from scipy.fftpack import ifft, fft, fftshift
from scipy.signal.windows import hann


#Radar parameters start here
bandwidth = 10e6
pulsewidth = 10e-5
alpha = 0.5 * bandwidth / pulsewidth # Chirp slope


#Sampling parameters start here
N = int(2 * bandwidth * pulsewidth) * 8 #Number of samples

#Todo why are we multyping by the pulsewidth...does this scale the time points?
t = linspace(-1 *pulsewidth,pulsewidth, N)

#Target parameters start here
ranges = [5000,100,1300,3000,4500]
range_floats = [float(r) for r in ranges]

s = zeros(N, dtype=complex)

#s is this return signal. The range_time_delay is there indicate the time where we sample a return
for r in ranges:
    range_time_delay = (t - 2.0 * r / c) #Making this a variable because it helps reinforce the concepts 
    s += exp(1j * 2.0 * pi * alpha * range_time_delay ** 2) #Sample is from when the pulse returns, using the radar distance return equation. 


# Transmit signal. The thing we're comparing for use in the matched filter
st = exp(1j * 2 * pi * alpha * t ** 2)

# Impulse response and matched filtering
Hf = fft(conj(st * hann(N, True))) #Applying a basic window without anything special about it
Si = fft(s)
so = fftshift(ifft(Si * Hf))


range_resolution = c * pulsewidth / 2
range_window = linspace(-1 * range_resolution, range_resolution, N) 

fig,ax = plt.subplots()

ax.plot(range_window, 20.0 * log10(abs(so) / N ))
ax.set_xlim(0, max(ranges) )
ax.set_ylim(-60, max( 20.0 * log10(abs(so) / N)))

# Set the x and y axis labels
ax.set_xlabel("Range (m)", size=12)
ax.set_ylabel("Amplitude (dBsm)", size=12)

# Turn on the grid
ax.grid(linestyle=':', linewidth=0.5)

# Set the plot title and labels
ax.set_title('Matched Filter Range Profile', size=14)

# Set the tick label size
ax.tick_params(labelsize=12)

fig,ax = plt.subplots()
ax.plot(s)