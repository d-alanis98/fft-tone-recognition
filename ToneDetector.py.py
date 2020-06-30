import copy
import soundfile
import matplotlib
import numpy, scipy
from scipy import arange
from matplotlib import pylab
from numpy import array, diff, where, split
#Módulo propio de FFT
from FFT import *
matplotlib.use('tkagg')

DEFAULT_NOISE_LEVEL = 10

def findHighestMagnitude(amplitudes, noise_level = DEFAULT_NOISE_LEVEL):
    
    splitter = 0
    # zero out low values in the magnitude array to remove noise (if any)
    amplitudes = numpy.asarray(amplitudes)        
    low_values_indices = amplitudes < noise_level  # Where values are low
    amplitudes[low_values_indices] = 0  # All low values will be zero out
    
    indices = []
    
    flag_start_looking = False
    
    both_ends_indices = []
    
    length = len(amplitudes)
    for i in range(length):
        if amplitudes[i] != splitter:
            if not flag_start_looking:
                flag_start_looking = True
                both_ends_indices = [0, 0]
                both_ends_indices[0] = i
        else:
            if flag_start_looking:
                flag_start_looking = False
                both_ends_indices[1] = i
                # add both_ends_indices in to indices
                indices.append(both_ends_indices)
                
    return indices

def extractFrequency(indices, freq_threshold=2):
    
    extracted_freqs = []
    
    for index in indices:
        freqs_range = freq_bins[index[0]: index[1]]
        avg_freq = round(numpy.average(freqs_range))
        
        if avg_freq not in extracted_freqs:
            extracted_freqs.append(avg_freq)

    # group extracted frequency by nearby=freq_threshold (tolerate gaps=freq_threshold)
    group_similar_values = split(extracted_freqs, where(diff(extracted_freqs) > freq_threshold)[0]+1 )
    
    # calculate the average of similar value
    extracted_freqs = []
    for group in group_similar_values:
        extracted_freqs.append(round(numpy.average(group)))
    
    print("freq_components", extracted_freqs)
    return extracted_freqs


file_path = 'samples/josue_u.wav'
print('Abriendo archivo: ', file_path)

audio_samples, sample_rate = soundfile.read(file_path, dtype='int16')
number_of_samples = len(audio_samples)
print('Audio samples: ', audio_samples)
print('Number of samples: ', number_of_samples)
print('Frecuencia de muestreo: ', sample_rate)

duration = round(number_of_samples/sample_rate, 2)
print('Audio duration: {0}s'.format(duration))

#Frecuencias que podemos detectar (sample_rate/2) (n * frequ)
freq_bins = numpy.arange(number_of_samples // 2) * sample_rate / number_of_samples
print('Frequency length  = ',len(freq_bins))
print('Frequency bins = ', freq_bins)

#fft_data = scipy.fft.fft(audio_samples)
fft_data = fft(audio_samples)
print('FFT length = ', len(fft_data))
print('FFT data = ', fft_data)

freq_bins = freq_bins[range(number_of_samples//2)]
normalization_data = fft_data/number_of_samples
amplitudes = normalization_data[range(len(fft_data)//2)]
amplitudes = numpy.abs(amplitudes)



def findFundamentalFrequency(amplitudes):
    #Definimos que todo lo que este por debajo de la mayor amplitud es ruido
    noise_level = max(amplitudes)
    indices = findHighestMagnitude(amplitudes=amplitudes, noise_level=noise_level)
    frequencies = extractFrequency(indices = indices)
    return frequencies




    
frequencies = findFundamentalFrequency(amplitudes)
print('Frequencies = ',frequencies)

x_axis = freq_bins
y_axis = amplitudes

pylab.plot(x_axis, y_axis, color='green')

pylab.xlabel('Freq(Hz)')
pylab.ylabel('Magnitude')
pylab.show()