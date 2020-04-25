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
        Dialog.resize(400, 300)

        self.ruta = ''

        self.lblFoto = QtWidgets.QLabel(Dialog)
        self.lblFoto.setGeometry(QtCore.QRect(10, 10, 150, 150))
        self.lblFoto.setText("")
        self.lblFoto.setObjectName("lblFoto")

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
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnElegir.setText(_translate("Dialog", "Seleccionar imagen"))
        self.btnEvaluar.setText(_translate("Dialog", "Evaluar foto"))

    def predict(self, file):
        longitud, altura = 100, 100
        modelo_clasificacion = os.path.relpath('data/modelo_clasificacion/modelo_clasificacion.h5')
        pesos_clasificacion = os.path.relpath('data/modelo_clasificacion/pesos_clasificacion.h5')

        modelo_lechuga = os.path.relpath('data/modelo_lechuga/modelo.h5')
        pesos_lechuga = os.path.relpath('data/modelo_lechuga/pesos.h5')

        modelo_plaga = os.path.relpath('data/modelo_plagas/modelo_plagas.h5')
        pesos_plaga = os.path.relpath('data/modelo_plagas/pesos_plagas.h5')

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
