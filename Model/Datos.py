from View.Interface import Ui_MainWindow
from segmentacion.Threshold_demo import Calibracion
import serial
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from controller.camara import Camara
from controller.micro import Micro
import cv2

class Datos(QtWidgets.QMainWindow):

    def __init__(self): #, ui, MainWindow) -> None:
        super().__init__()
        #Llamo a la clase main window del main script, ademas
        #llamo el objeto de la clase Ui_MainWindow obtenida en el 
        #main script
        
        #>>>>-----Definicion Ventana Principal-----<<<<<
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonHome.setEnabled(True)
        self.ui.pushButtonCalibracion.setEnabled(True)
        self.ui.lineEditId.setEnabled(True)
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.pushButtonStart.setStyleSheet("background-color: rgb(168, 168, 168);\n"
        "border-radius: 15%;")
        self.ui.comboBoxVariedad.setCurrentIndex(-1)
        self.comboInfo = ""


        #Objetos Controladores
        self.driver = Micro(ui=self.ui) #----COMUNICACION----
        self.camara = Camara(ui=self.ui,driver=self.driver) #----COMUNICACION----
        self.calibracion = Calibracion()

        #>>>>-----INICIO DEL HILO DE LA CAMARA-----<<<<
        self.camara.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        self.hiloCamara = threading.Thread(target=self.camara.startCamara)
        self.hiloCamara.start()

        # #VARIABLES DE CONTROL:
        self.modoPruebas = False


        #SIGNALS TO SLOTS:
        self.ui.pushButtonStart.clicked.connect(self.startButton)
        self.ui.pushButtonInfo.clicked.connect(self.info)
        self.ui.pushButtonHome.clicked.connect(self.driver.home)
        self.ui.pushButtonResultados.clicked.connect(self.camara.fotoWindow)
        self.ui.comboBoxVariedad.currentIndexChanged.connect(self.dataChange)
        self.ui.pushButtonCalibracion.clicked.connect(self.modoCalibracion)


    #>>>>-----Presionar Boton Scan-----<<<<<
    def startButton(self):

        self.ui.pushButtonStart.setEnabled(True)
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.pushButtonStart.setStyleSheet("background-color: rgb(168, 168, 168);\n"
        "border-radius: 15%;")
        self.camara.threadFlagScan.set()
        # self.camara.scanning = True


    def info(self):

        self.ui.pushButtonStart.setEnabled(True)
        self.ui.pushButtonStart.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.547, y1:0.983, x2:0.532105, y2:0, stop:0.0684211 rgba(0, 157, 0, 255), stop:1 rgba(185, 244, 158, 255));\n"
        "border-radius: 15%;")
        str1 = self.ui.lineEditId.text()
        self.ui.labelId.setText(str1)
        self.ui.labelVariedad.setText(self.comboInfo)
        self.ui.comboBoxVariedad.setCurrentIndex(-1)


    def dataChange(self):
        
        try:
            if self.ui.comboBoxVariedad.currentIndex() != -1:
                self.comboInfo = self.ui.comboBoxVariedad.currentText() 
            else:
                pass
        except:
            print('mal funcionamiento comboBox')
        
    def modoCalibracion(self):
        
        self.calibracion.runCalibracion()

#>>>>-----Evento de cierre de programa-----<<<<
    def closeEvent(self,event):

        try:
            
            self.camara.stop()
            self.hiloCamara.join()
            self.driver.communication.close()
            cv2.destroyAllWindows()
            print('*******Finalizado*******')
        except Exception as e:
            print(f"ERROR AL FINALIZAR: {e}")