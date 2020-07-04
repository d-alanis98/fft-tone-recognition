import copy
import soundfile
#import matplotlib
import numpy, scipy
from scipy import arange
#from matplotlib import pylab
from numpy import array, diff, where, split
#Módulo propio de FFT
from FFT import *
#Frecuencias de las vocales
from AverageVocalFrequencies import *

#Constantes
PATH_PREFIX = 'samples/%s'
DEFAULT_NOISE_LEVEL = 10

#Variables globales
fft_data = []
amplitudes = []
sample_rate = 0
audio_samples = []
frequency_axis = []
number_of_samples = 0
fundamental_frequency = 0



def readAudioFile(file_name):
    global sample_rate, audio_samples, number_of_samples
    #Establecemos la ruta al archivo, el cual se encuentra en el directorio samples
    file_path = PATH_PREFIX % file_name
    #Obtenemos información del archivo, en concreto, las muestras de audio y la frecuencia de muestreo
    audio_samples, sample_rate = soundfile.read(file_path, dtype = 'int16')
    number_of_samples = len(audio_samples)

def setFrequencyAxis():
    global frequency_axis
    #Frecuencias que podemos detectar y lo llenamos con su respectiva frequencia (cada salto es de: freq_muestreo/número de muestras)
    frequency_axis = numpy.arange(number_of_samples) * sample_rate / number_of_samples

def applyFFT():
    global fft_data
    #Aplicamos la fft proveniente de nuestro módulo FFT
    fft_data = fft(audio_samples)
    #fft_data = scipy.fft.fft(audio_samples)

def getSignalData():
    global amplitudes, frequency_axis
    #Obtenemos la parte útil de la señal, la cual es de la mitad de las muestras, pues según el teorema de Nyquist, fN = 2fmax
    frequency_axis = frequency_axis[range(number_of_samples//2)]
    amplitudes = fft_data[range(len(fft_data)//2)]
    #Obtenemos el valor absoluto de los elementos del array de amplitudes
    amplitudes = numpy.abs(amplitudes)

def getFundamentalFrequencyFromSamples(amplitudes, noise_level = DEFAULT_NOISE_LEVEL):
    #Creamos una copia del array para garantizar inmutabilidad
    amplitudes = numpy.asarray(amplitudes)   
    #Definimos la condición para determinar que valores se convertirán en 0
    low_values_positions = amplitudes < noise_level  
    #Dicha condición es que toda amplitud que sea menor a lo que se definió como ruido se hace 0
    amplitudes[low_values_positions] = 0
    
    length = len(amplitudes)

    highest_amplitude_index = -1
    #Buscamos el único elemento en el array de amplitudes que no es 0 (el cual es la magnitud más grande)
    for index in range(length):
        if amplitudes[index] != 0:
            #Una vez que se encuentra, se obtiene su índice y se sale del bucle
            highest_amplitude_index = index
            break
    #Válidamos que se haya encontrado el índice (cosa que debe pasar, pero la validación no esta de más)
    if highest_amplitude_index == -1:
        return None
    #Retornamos la frecuencia fundamental, la cual es la que se encuentra en el mismo índice en el que se encuentra la magnitud más grande en el array de magnitudes
    return frequency_axis[highest_amplitude_index]


def setFundamentalFrequency():
    global fundamental_frequency
    #Definimos que todo lo que este por debajo de la mayor amplitud en el array de amplitudes es ruido
    noise_level = np.max(amplitudes)
    #Obtenemos la frecuencia fundamental suministrando los parámetros necesarios (array de amplitudes y nivel de ruido que acabamos de definir)
    fundamental_frequency = getFundamentalFrequencyFromSamples(amplitudes = amplitudes, noise_level = noise_level)

def getResultData(file_name):
    return{
        "file_name": file_name,
        "sampling_frequency": sample_rate,
        "fundamental_frequency": fundamental_frequency
    }

def mergeDictionaries(dictionary1, dictionary2):
    return {**dictionary1, **dictionary2} 

def findNearestVocalFrequency():
    male_frequencies = vocal_frequencies['male']
    female_frequencies = vocal_frequencies['female']
    male_padding = 9999
    male_vocal_index = -1
    female_padding = 9999
    female_vocal_index = -1
    for index in range(5):
        #Obtenemos el padding, es decir, la diferencia entre la frecuencia fundamenteal obtenida y el valor de la frecuencia fundamental promedio de esa vocal para hombres y mujeres
        new_male_padding = abs(male_frequencies[vocals[index]] - fundamental_frequency)
        new_female_padding = abs(female_frequencies[vocals[index]] - fundamental_frequency)
        #Si el padding es menor, se actualiza tanto este valor como su índice
        if new_male_padding < male_padding:
            male_padding = new_male_padding
            male_vocal_index = index
        #Lo mismo aplica para el padding de las vocales femeninas
        if new_female_padding < female_padding:
            female_padding = new_female_padding
            female_vocal_index = index
    #Finalmente, hacemos la comparación para ver cual padding es menor, y eso determinará tanto la vocal como el género
    if male_padding <= female_padding:
        return {
            "result_vocal": vocals[male_vocal_index],
            "result_gender": "male"
        }
    else:
        return {
            "result_vocal": vocals[female_vocal_index],
            "result_gender": "female"
        }



"""
Función principal, invoca a las demás conforme se va requiriendo para analizar el archivo y obtener su frecuencia fundamental
"""
def analyzeAudioFile(file_name):
    readAudioFile(file_name)
    setFrequencyAxis()
    applyFFT()
    getSignalData()
    setFundamentalFrequency()
    print('Frecuencia fundamental = ', fundamental_frequency)
    partialResult = getResultData(file_name)
    nearestVocalData = findNearestVocalFrequency()
    return mergeDictionaries(partialResult, nearestVocalData)

#print(analyzeAudioFile('josue_o.wav'))



"""
#Gráfica
x_axis = frequency_axis
y_axis = amplitudes

pylab.plot(x_axis, y_axis, color='green')

pylab.xlabel('Freq(Hz)')
pylab.ylabel('Magnitude')
pylab.show()

"""