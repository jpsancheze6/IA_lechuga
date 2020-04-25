from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Analizador de Lechugas")
        Dialog.resize(400, 300)

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

    def evaluarFoto(self):
        print('chipi')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnElegir.setText(_translate("Dialog", "Seleccionar imagen"))
        self.btnEvaluar.setText(_translate("Dialog", "Evaluar foto"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
