from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image
import keras
import tensorflow as tf
import numpy as np
import os


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Analizador de Lechugas")
        Dialog.resize(400, 280)

        self.ruta = ''

        self.lblFoto = QtWidgets.QLabel(Dialog)
        self.lblFoto.setGeometry(QtCore.QRect(10, 10, 150, 150))
        self.lblFoto.setText("")
        self.lblFoto.setObjectName("lblFoto")

        self.lblDesc = QtWidgets.QLabel(Dialog)
        self.lblDesc.setGeometry(QtCore.QRect(10, 170, 380, 100))
        self.lblDesc.setText("")
        self.lblDesc.setObjectName("lblDesc")

        self.btnElegir = QtWidgets.QPushButton(Dialog)
        self.btnElegir.setGeometry(QtCore.QRect(230, 20, 141, 23))
        self.btnElegir.setObjectName("btnElegir")

        self.btnEvaluar = QtWidgets.QPushButton(Dialog)
        self.btnEvaluar.setGeometry(QtCore.QRect(230, 60, 141, 23))
        self.btnEvaluar.setObjectName("btnEvaluar")

        self.btnElegir.clicked.connect(self.seleccionarImagen)
        self.btnEvaluar.clicked.connect(self.evaluarFoto)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def seleccionarImagen(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filename = dlg.selectedFiles()
            # Colocar imagen en lblFoto
            imagen = QPixmap(str(filename[0])).scaled(150, 150)
            self.lblFoto.setPixmap(imagen)
            self.ruta = filename[0]

    def evaluarFoto(self):
        self.predict(self.ruta)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Evaluador de fases lechuga"))
        self.btnElegir.setText(_translate("Dialog", "Seleccionar imagen"))
        self.btnEvaluar.setText(_translate("Dialog", "Evaluar foto"))

    def predict(self, file):
        texto = ''
        texto = 'La planta presenta las siguientes características:\n\n'
        longitud, altura = 100, 100
        modelo_clasificacion = os.path.relpath('data/modelo_clasificacion/modelo_clasificacion.h5')
        pesos_clasificacion = os.path.relpath('data/modelo_clasificacion/pesos_clasificacion.h5')

        modelo_lechuga = os.path.relpath('data/modelo_lechuga/modelo.h5')
        pesos_lechuga = os.path.relpath('data/modelo_lechuga/pesos.h5')

        modelo_plaga = os.path.relpath('data/modelo_plagas/modelo_plagas.h5')
        pesos_plaga = os.path.relpath('data/modelo_plagas/pesos_plagas.h5')

        modelo_edad = os.path.relpath('data/modelo_fecha/modelo.h5')
        pesos_edad = os.path.relpath('data/modelo_fecha/pesos.h5')

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
            texto = texto + 'Si es lechuga.\n'
            if respuesta_1 == 0:
                print('Fase 1')

                texto = texto + 'Fase 1.\n'
                arreglo_2 = red_plagas.predict(x)
                resultado_2 = arreglo_2[0]
                respuesta_2 = np.argmax(resultado_2)
                if respuesta_2 == 0:
                    print('La planta presenta plagas')
                    texto = texto + 'Presenta plagas.\n'
                elif respuesta_2 == 1:
                    print('La planta se encuenta en buen estado')
                    texto = texto + 'Se encuentra en buen estado.\n'
                
                arreglo_3 = red_fecha.predict(x)
                resultado_3 = arreglo_3[0]
                respuesta_3 = np.argmax(resultado_3)
                if respuesta_3 == 0:
                    texto = texto + 'Edad de 1 - 10 días.'
                elif respuesta_3 == 1:
                    texto = texto + 'Edad de 11 - 27 días.'
                elif respuesta_3 == 2:
                    texto = texto + 'Edad de 28 - 43 días.'
                elif respuesta_3 == 3:
                    texto = texto + 'Edad de 44 - 60 días.'
                elif respuesta_3 == 4:
                    texto = texto + 'Edad de 61 - 76 días.'
                elif respuesta_3 == 5:
                    texto = texto + 'Edad de 77 - 81 días.'
                elif respuesta_3 == 6:
                    texto = texto + 'Edad de 82 - 86 días.'

            elif respuesta_1 == 1:
                print('Fase 2')

                texto = texto + 'Fase 2.\n'
                arreglo_2 = red_plagas.predict(x)
                resultado_2 = arreglo_2[0]
                respuesta_2 = np.argmax(resultado_2)
                if respuesta_2 == 0:
                    print('La planta presenta plagas')
                    texto = texto + 'Presenta plagas.\n'
                elif respuesta_2 == 1:
                    print('La planta se encuenta en buen estado')
                    texto = texto + 'Se encuentra en buen estado.\n'
                
                arreglo_3 = red_fecha.predict(x)
                resultado_3 = arreglo_3[0]
                respuesta_3 = np.argmax(resultado_3)
                if respuesta_3 == 0:
                    texto = texto + 'Edad de 1 - 10 días.'
                elif respuesta_3 == 1:
                    texto = texto + 'Edad de 11 - 27 días.'
                elif respuesta_3 == 2:
                    texto = texto + 'Edad de 28 - 43 días.'
                elif respuesta_3 == 3:
                    texto = texto + 'Edad de 44 - 60 días.'
                elif respuesta_3 == 4:
                    texto = texto + 'Edad de 61 - 76 días.'
                elif respuesta_3 == 5:
                    texto = texto + 'Edad de 77 - 81 días.'
                elif respuesta_3 == 6:
                    texto = texto + 'Edad de 82 - 86 días.'

            elif respuesta_1 == 2:
                print('Fase 3')

                texto = texto + 'Fase 3.\n'
                arreglo_2 = red_plagas.predict(x)
                resultado_2 = arreglo_2[0]
                respuesta_2 = np.argmax(resultado_2)
                if respuesta_2 == 0:
                    print('La planta presenta plagas')
                    texto = texto + 'Presenta plagas.\n'
                elif respuesta_2 == 1:
                    print('La planta se encuenta en buen estado')
                    texto = texto + 'Se encuentra en buen estado.\n'
                
                arreglo_3 = red_fecha.predict(x)
                resultado_3 = arreglo_3[0]
                respuesta_3 = np.argmax(resultado_3)
                if respuesta_3 == 0:
                    texto = texto + 'Edad de 1 - 10 días.'
                elif respuesta_3 == 1:
                    texto = texto + 'Edad de 11 - 27 días.'
                elif respuesta_3 == 2:
                    texto = texto + 'Edad de 28 - 43 días.'
                elif respuesta_3 == 3:
                    texto = texto + 'Edad de 44 - 60 días.'
                elif respuesta_3 == 4:
                    texto = texto + 'Edad de 61 - 76 días.'
                elif respuesta_3 == 5:
                    texto = texto + 'Edad de 77 - 81 días.'
                elif respuesta_3 == 6:
                    texto = texto + 'Edad de 82 - 86 días.'

        elif respuesta == 1:
            print('No es lechuga')
            texto = texto + 'No es lechuga.\n'
        self.lblDesc.setText(texto)
        return respuesta

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
