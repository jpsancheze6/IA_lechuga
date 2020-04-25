import sys
import os
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from tensorflow.python.framework.ops import disable_eager_execution

disable_eager_execution()                       # Deshabilitar para evitar problemas con Adam

os.system('clear')

K.clear_session()                               # Terminar todas las sesiones activas de keras.

data_entrenamiento = os.path.relpath('data/entrenamiento_plagas')     # Ruta de la carpeta de las imágenes de entrenamiento
data_validacion = os.path.relpath('data/validacion_plagas')           # Ruta de la carpeta de las imágenes de prueba o validación

"""
    Parámetros de la red neuronal
"""

epocas = 5                                     # Cantidad de épocas que va a evaluar la red neuronal
altura, longitud = 100, 100                     # Tamaño de las imágenes que van a evaluar
batch_size = 32                                 # Número de imágenes a procesar por cada época
pasos = 1000                                    # Número de veces a procesar las imágenes en cada época
pasos_validacion = 500                          # Por cada época valida que la red esté funcionando bien
filtrosConv1 = 32                               # Profunidad después de la convolución 1
filtrosConv2 = 64                               # Profunidad después de la convolución 2
size_filtro1 = (3, 3)                           # Filtro convolución 1
size_filtro2 = (2, 2)                           # Filtro convolución 2
size_pool = (2, 2)                              # Tamaño de filtro en el max pooling
clases = 2                                      # Número de elementos que se van a examinar (gato, perro, gorila)
lr = 0.0005                                     # Constante de aprendizaje

"""
    Preprocesamiento de las imágenes antes de pasarselas a la red neuronal
"""

entrenamiento_datagen = ImageDataGenerator(     # Modificar imágenes de el set de entrenamiento
    rescale = 1./255,                           # Reescalar los colores para que estén en el rango de [0-1]
    shear_range = 0.3,                          # Cambiar la orientación de las imágenes para que no estén siempre verticales
    zoom_range = 0.3,                           # Zoom para que no aparezca el objero siempre completo
    horizontal_flip = True                      # Invertir horizontalmente
)

validacion_datagen = ImageDataGenerator(        # Modificar imágenes de el set de validación
    rescale = 1./255                            # Reescalar los colores para que estén en el rango de [0-1]
)

# Generación de imágenes para el entrenamiento y validación

imagen_entrenamiento = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,                         # Carpeta de imágenes de entrenamiento
    target_size = (altura, longitud),           # Tamaño a leer de las imágenes
    batch_size = batch_size,                    # Imágenes a procesar por cada época
    class_mode = 'categorical'                  # Colocar categorías a nuestras imágenes
)

imagen_validacion = validacion_datagen.flow_from_directory(
    data_validacion,                            # Carpeta de imágenes de validación
    target_size = (altura, longitud),           # Tamaño a leer de las imágenes
    batch_size = batch_size,                    # Imágenes a procesar por cada época
    class_mode = 'categorical'                  # Colocar categorías a nuestras imágenes
)

"""
    Creación de la estructura de la red
"""

red = Sequential()                              # Red convolucionales van a ser secuenciales, una capa tras otra

red.add(Convolution2D(                          # La primera capa va a ser una convolución 
    filtrosConv1,                               # Número de filtros a tener en la primera convolución
    size_filtro1,                               # Tamaño de filtro definido previamente
    padding = 'same',                           # Filtro en las esquinas
    input_shape=(altura, longitud, 3),          # Tamaño de entradas de las imágenes y el filtro (3, RGB)
    activation = 'relu')                        # Función de activación
)

red.add(MaxPooling2D(                           # Primera capa de MaxPooling
    pool_size = size_pool                       # Tamaño del filtro del MaxPooling
))

red.add(Convolution2D(
    filtrosConv2,                               # Número de filtros a tener en la segunda convolución
    size_filtro2,                               # Tamaño de filtro definido previamente
    padding = 'same',                           # Filtro en las esquinas
    activation = 'relu')                        # Función de activación
)

red.add(MaxPooling2D(                           # Segunda capa de MaxPooling
    pool_size = size_pool                       # Tamaño del filtro del MaxPooling
))

red.add(Flatten())                              # Covertir imagen muy pequeña a una sola información, aplanar

red.add(Dense(
    256,                                        # Número de neuronas
    activation = 'relu'                         # Función de activación
))

red.add(Dropout(
    0.50                                        # Se apaga la cantidad en porcentaje de neuronas, para evitar sobreajustar
))

red.add(Dense(
    clases,                                     # Número de neuronas de salida
    activation = 'softmax'                      # Nos da los valores en porcentaje de las posibles soluciones
))

red.compile(                                    # Parámetros a utilizar para optimizar el algoritmo
    loss = 'categorical_crossentropy',          # Función para analizar que tan bien y que tan mal va el aprendizaje
    optimizer = optimizers.Adam(lr = lr),       # Optimizador
    metrics = ['accuracy']                      # Métrica para calificar que tan bien está aprendiendo la red neuronal
)

red.fit(
    imagen_entrenamiento,                       # Valores para realizar el entranamiento
    steps_per_epoch = pasos,                    # Pasos por la época que se va a realizar
    epochs = epocas,                            # Número de épocas que se van a tener en el entrenamiento
    validation_data = imagen_validacion,        # Valores para realizar la validación
    validation_steps = pasos_validacion         # Pasos para la validación
)

"""
    Guardar la información en un archivo
"""

dir = os.path.relpath('data/modelo_plagas/')

if not os.path.exists(dir):
    os.mkdir(dir)

red.save(os.path.relpath('data/modelo_plagas/modelo_plagas.h5'))                  # Guardar el modelo con los resultados
red.save_weights(os.path.relpath('data/modelo_plagas/pesos_plagas.h5'))           # Guardar los pesos del modelo
