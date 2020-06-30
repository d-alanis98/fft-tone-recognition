import math
import numpy as np
#GUI


#Constantes matemáticas
e = math.e
pi = math.pi

"""
Funcion que devuelve los items impares de un array (impares refiriendonos a su indice, por eso empezamos en a[0], que corresponde al primer elemento del array, y vamos de 2 en 2)
"""
def get_even(input):
    return input[::2]

"""
Funcion que devuelve los items pares de un array (pares refiriendonos a su indice, por eso empezamos en a[1], que corresponde al segundo elemento del array, y vamos de 2 en 2)
"""
def get_odd(input):
    return input[1::2]

"""
Función que devuelve únicamente la parte real de un número complejo, recibe un array de números de tipo complex
"""
def get_real_part(complex_samples):
    number_of_samples = len(complex_samples)
    result = np.zeros(number_of_samples)
    for i in range(0, number_of_samples):
        result[i] = complex_samples[i].real 
    return result

"""
Obtiene el peso (2ipi/N), con un factor de -1 (si es para la transformada directa) o de 1 (si es para la inversa)
"""
def get_wn(number_of_samples, inverse = False):
    factor = -1
    if inverse:
        factor = 1
    return e ** ((2 * factor * pi * complex(0, 1)) / number_of_samples)

"""
Algoritmo base, lo utilizan ambos métodos (fft e ifft), donde se recibe un parámetro adicional a las muestras sobre las que se 
efectuará la operación, el cual es una bandera para saber si se trata de la transformada inversa, si esta bandera esta en estado
lógico falso se sobreentiende que se trata de la transformada directa
"""
def algorithm(samples, inverse = False):
    #Obtenemos el número de muestras (N)
    number_of_samples = len(samples)
    #Obtenemos el índice que indica la mitad, considerando que N siempre será potencia de 2
    half = number_of_samples // 2 
    #Caso base, donde solo tenemos 1 elemento, entonces simplemente lo retorna
    if number_of_samples == 1:
        return samples
    #Obtenemos el peso wn de la secuencia (wn^1)
    wn = get_wn(number_of_samples, inverse)
    #Declaramos la variable que contendrá el acumulador de pesos para cada iteración
    w = 1 #Inicializado en 1 (w^0)
    #Se separa el array en pares e impares
    even = get_even(samples) 
    odd = get_odd(samples)
    #Se obtiene cada mitad por el método de divide y vencerás (para formar la mariposa posteriormente)
    fft_even = algorithm(even)
    fft_odd = algorithm(odd)
    #Llenamos un array de tamaño N de ceros (de tipo complejo, 0 + 0j)
    fft_result = np.zeros(number_of_samples, dtype = complex) 
    #Ciclo para formar la mariposa y efectuar las operaciones en esta
    for i in range(0, half):
        fft_result[i] = fft_even[i] + w * fft_odd[i] #De 0 a N/2 es fft(pares) + w*fft(impares) (la parte impar tiene una ponderación de w)
        fft_result[i + half] = fft_even[i] - w * fft_odd[i] #De N/2 a N es fft(pares) - w*fft(impares) (la parte impar tiene una ponderación de -w)
        w = w * wn #Se va acumulando w, ya que en cada iteración se eleva a la potencia i, esto sería lo mismo que w = wn ** i
    return fft_result  

"""
Función que realiza el cálculo de la FFT haciendo uso de la función algorithm en modo directo (inverse = False por defecto)
"""
def fft(samples):
    return algorithm(samples)

"""
Función que realiza el cálculo de la IFFT haciendo uso de la función algorithm en modo inverso (inverse = True), para posteriormente
obtener solo la parte real, ya que quedan algunos residuos infinitesimales de la parte imaginaria.
"""
def ifft(samples):
    number_of_samples = len(samples)
    complex_result = (1 / number_of_samples) * algorithm(samples, inverse = True)
    return get_real_part(complex_result)

