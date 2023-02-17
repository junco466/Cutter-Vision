# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'presentarFotos.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Presentacion(object):
    def setupUi(self, Presentacion):
        Presentacion.setObjectName("Presentacion")
        Presentacion.setWindowModality(QtCore.Qt.NonModal)
        Presentacion.resize(1525, 736)
        Presentacion.setMaximumSize(QtCore.QSize(16777215, 881))
        self.centralwidget = QtWidgets.QWidget(Presentacion)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(80)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelImg0 = QtWidgets.QLabel(self.centralwidget)
        self.labelImg0.setMinimumSize(QtCore.QSize(0, 400))
        self.labelImg0.setMaximumSize(QtCore.QSize(450, 600))
        self.labelImg0.setAutoFillBackground(False)
        self.labelImg0.setStyleSheet("background-color: gray;")
        self.labelImg0.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelImg0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelImg0.setLineWidth(10)
        self.labelImg0.setText("")
        self.labelImg0.setScaledContents(True)
        self.labelImg0.setObjectName("labelImg0")
        self.horizontalLayout_2.addWidget(self.labelImg0)
        self.labelImg1 = QtWidgets.QLabel(self.centralwidget)
        self.labelImg1.setMaximumSize(QtCore.QSize(450, 600))
        self.labelImg1.setStyleSheet("background-color: gray;")
        self.labelImg1.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelImg1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelImg1.setLineWidth(10)
        self.labelImg1.setText("")
        self.labelImg1.setScaledContents(True)
        self.labelImg1.setObjectName("labelImg1")
        self.horizontalLayout_2.addWidget(self.labelImg1)
        self.labelImg2 = QtWidgets.QLabel(self.centralwidget)
        self.labelImg2.setMaximumSize(QtCore.QSize(450, 600))
        self.labelImg2.setStyleSheet("background-color: gray;")
        self.labelImg2.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelImg2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelImg2.setLineWidth(10)
        self.labelImg2.setMidLineWidth(1)
        self.labelImg2.setText("")
        self.labelImg2.setScaledContents(True)
        self.labelImg2.setObjectName("labelImg2")
        self.horizontalLayout_2.addWidget(self.labelImg2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        Presentacion.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Presentacion)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1525, 26))
        self.menubar.setObjectName("menubar")
        Presentacion.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Presentacion)
        self.statusbar.setObjectName("statusbar")
        Presentacion.setStatusBar(self.statusbar)

        self.retranslateUi(Presentacion)
        QtCore.QMetaObject.connectSlotsByName(Presentacion)

    def retranslateUi(self, Presentacion):
        _translate = QtCore.QCoreApplication.translate
        Presentacion.setWindowTitle(_translate("Presentacion", "Fotos Procesadas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Presentacion = QtWidgets.QMainWindow()
    ui = Ui_Presentacion()
    ui.setupUi(Presentacion)
    Presentacion.show()
    sys.exit(app.exec_())

