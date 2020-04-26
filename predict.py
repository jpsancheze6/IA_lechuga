#from keras.preprocessing.image import load_img, img_to_array
import keras
import tensorflow as tf
import numpy as np
import os

def predict(file):
    longitud, altura = 100, 100
    modelo_clasificacion = os.path.relpath('data/modelo_clasificacion/modelo_clasificacion.h5')
    pesos_clasificacion = os.path.relpath('data/modelo_clasificacion/pesos_clasificacion.h5')

    modelo_lechuga = os.path.relpath('data/modelo_lechuga/modelo.h5')
    pesos_lechuga = os.path.relpath('data/modelo_lechuga/pesos.h5')

    modelo_plaga = os.path.relpath('data/modelo_plagas/modelo_plagas.h5')
    pesos_plaga = os.path.relpath('data/modelo_plagas/pesos_plagas.h5')

    modelo_edad = os.path.relpath('data/modelo_fecha/modelo_clasificacion.h5')
    pesos_edad = os.path.relpath('data/modelo_fecha/pesos_clasificacion.h5')

    red_fecha = tf.keras.models.load_model(modelo_edad)
    red_fecha.load_weights(pesos_edad)

    red_clasificacion = tf.keras.models.load_model(modelo_clasificacion)
    red_clasificacion.load_weights(pesos_clasificacion)

    red_lechuga = tf.keras.models.load_model(modelo_lechuga)        # Carga el modelo que se obtuvo previamente
    red_lechuga.load_weights(pesos_lechuga)                         # Carga los pesos que se encontraron en el entrenamiento

    red_plagas = tf.keras.models.load_model(modelo_plaga)
    red_plagas.load_weights(pesos_plaga)
    os.system('clear')
    x = keras.preprocessing.image.load_img(file, target_size = (longitud, altura))
    x = keras.preprocessing.image.img_to_array(x)
    x = np.expand_dims(x, axis = 0)

    arreglo = red_clasificacion.predict(x)                    # Devuelve [[1, 0, 0]], donde 1 es el valor correcto
    resultado = arreglo[0]
    respuesta = np.argmax(resultado)
    
    if respuesta == 0:
        print('Si es lechuga')
        arreglo_1 = red_lechuga.predict(x)
        resultado_1 = arreglo_1[0]
        respuesta_1 = np.argmax(resultado_1)
        if respuesta_1 == 0:
            print('Fase 1')

            arreglo_2 = red_plagas.predict(x)
            resultado_2 = arreglo_2[0]
            respuesta_2 = np.argmax(resultado_2)
            if respuesta_2 == 0:
                print('La planta presenta plagas')
            elif respuesta_2 == 1:
                print('La planta se encuenta en buen estado')

        elif respuesta_1 == 1:
            print('Fase 2')

            arreglo_2 = red_plagas.predict(x)
            resultado_2 = arreglo_2[0]
            respuesta_2 = np.argmax(resultado_2)
            if respuesta_2 == 0:
                print('La planta presenta plagas')
            elif respuesta_2 == 1:
                print('La planta se encuenta en buen estado')

        elif respuesta_1 == 2:
            print('Fase 3')

            arreglo_2 = red_plagas.predict(x)
            resultado_2 = arreglo_2[0]
            respuesta_2 = np.argmax(resultado_2)
            if respuesta_2 == 0:
                print('La planta presenta plagas')
            elif respuesta_2 == 1:
                print('La planta se encuenta en buen estado')

    elif respuesta == 1:
        print('No es lechuga')
    return respuesta

# Predice 
predict(os.path.relpath('test/p3.jpg'))