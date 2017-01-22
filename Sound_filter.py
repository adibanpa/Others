# PHY407 Lab 5 Question 2
# Jenny Wu (1000565168), Parham Adiban (1000639446)
'''
Apply a low-pass filter (880Hz) to a sound file.
'''
#The scipy.io.wavfile allows you to read and write .wav files
from __future__ import division, print_function
from scipy.io.wavfile import read, write
from numpy import empty, arange
from pylab import *

#read the data into two stereo channels
#sample is the sampling rate, data is the data in each channel,
#  dimensions [2, nsamples]
sample, data = read('GraviteaTime.wav')
#sample is the sampling frequency, 44100 Hz
#separate into channels
channel_0 = data[:,0]
channel_1 = data[:,1]
N_Points = len(channel_0)

time = arange(N_Points)*1.0/sample #Define a time array with dt corresponding to the given sampling rate

#Plot the the full timeseries of the soundfile
figure(0)

subplot(2, 1, 1)
plot(time, channel_0)
title('Timeseries from Sound File', size = 20)
ylabel('Channel 0', size = 15)

subplot(2, 1, 2)
plot(time, channel_1)
ylabel('Channel 1', size = 15)
xlabel('Time (s)', size  = 15)

tight_layout()

#Plot the timeseries for the segment between 10ms to 40ms
figure(1)

subplot(2, 1, 1)
plot(time, channel_0)
title('Segment of Total Timeseries', size = 20)
ylabel('Channel 0', size = 15)
xlim([0.01, 0.04])

subplot(2, 1, 2)
plot(time, channel_1)
ylabel('Channel 1', size = 15)
xlabel('Time (s)', size  = 15)
xlim([0.01, 0.04])

tight_layout()

#Define frequency array corresponding to the given sampling rate
freq = sample*arange(N_Points/2 + 1)/N_Points

#Define the terms for the fourier transform of each channel
channel0_t = rfft(channel_0)
channel1_t = rfft(channel_1)

#Plot of the fourier tranform as a function of frequency
figure(2)
subplot(2, 1, 1)
plot(freq, abs(channel0_t)) #amplitude of coefficients 
title('Original Fourier Coefficients', size = 20)
ylabel('Channel 0', size = 15)
xlim(xmin = -100)   #shift the minimum x-axis value so the point at 0 is easier to see

subplot(2, 1, 2)
plot(freq, abs(channel1_t))
ylabel('Channel 1', size = 15)
xlabel('Frequency (Hz)', size = 15)
xlim(xmin = -100)

tight_layout()

#Create copy of transformed data
ch0_cleaned = channel0_t
ch1_cleaned = channel1_t

#Filter all frequencies >880Hz using boolean masking
ch0_cleaned[freq>880] = 0
ch1_cleaned[freq>880] = 0

#Plot of the filtered fourier transform
figure(3)

subplot(2, 1, 1)
plot(freq, abs(ch0_cleaned))      
title('Filtered Fourier Coefficients', size = 20)
axvline(880, ls = '--')           #add a vertical line to indicate point at which filtering began
ylabel('Channel 0', size = 15)
xlim(xmin = -100)

subplot(2, 1, 2)
plot(freq, abs(ch1_cleaned))
axvline(880, ls = '--')
ylabel('Channel 1', size = 15)
xlabel('Frequency (Hz)', size = 15)
xlim(xmin = -100)

tight_layout()

#Reverse fourier transform to find the filtered timeseries
channel_0_out = irfft(ch0_cleaned)
channel_1_out = irfft(ch1_cleaned)

#Plot the filtered timeseries for the segment between 10ms to 40ms
figure(4)

subplot(2, 1, 1)
plot(time, channel_0_out)
title('Segment of Filtered Timeseries', size = 20)
ylabel('Channel 0', size = 15)
xlim([0.01, 0.04])

subplot(2, 1, 2)
plot(time, channel_1_out)
xlim([0.01, 0.04])
ylabel('Channel 1', size = 15)
xlabel('Time (s)', size = 15)

tight_layout()

show()

#this creates an empty array data_out with the
#same shape as "data" (2 x N_Points) and the same
#type as "data" (int16)
data_out = empty(data.shape, dtype = data.dtype)
#fill data_out
data_out[:,0] = channel_0_out
data_out[:,1] = channel_1_out
# write to file
write('GraviteaTime_lpf.wav', sample, data_out)