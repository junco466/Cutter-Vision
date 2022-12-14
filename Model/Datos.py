from View.Interface import Ui_MainWindow
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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.labelPrueba.setText("OFF")
        self.ui.pushButtonHome.setEnabled(True)


        #Objetos Controladores
        self.driver = Micro(ui=self.ui) #----COMUNICACION----
        self.camara = Camara(ui=self.ui,driver=self.driver) #----COMUNICACION----


        #>>>>-----INICIO DEL HILO DE LA CAMARA-----<<<<
        self.camara.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        self.hiloCamara = threading.Thread(target=self.camara.startCamara)
        self.hiloCamara.start()

        # #VARIABLES DE CONTROL:
        self.modoPruebas = False


        #SIGNALS TO SLOTS:
        self.ui.pushButtonStart.clicked.connect(self.startButton)
        self.ui.pushButtonPruebas.clicked.connect(self.pruebas)
        self.ui.pushButtonComando.clicked.connect(self.enviar)
        self.ui.pushButtonFoto.clicked.connect(self.camara.take_photo)
        self.ui.pushButtonHome.clicked.connect(self.driver.home)

        #Metodo para cerrar el hilo, y que no se quede ejecutando
        #como proceso de segundo plano, infinitamente

        # #objeto serial, para comenzar comunicacion serial con microcontrolador
        # self.communication = serial.Serial("COM5",115200,timeout=2)
        # time.sleep(1.0)

        # self.valueVel = 0
        # #Signals/Slots
        # self.ui.pushButtonEnviar.clicked.connect(self.enviar)

        # self.isRun = True
        # self.hilo1.start()

        #self.hiloClose.start()


        #****Presionar Boton Start****
    def startButton(self):

        self.ui.pushButtonStart.setEnabled(False)
        self.ui.pushButtonStart.setStyleSheet("background-color: rgb(168, 168, 168);\n"
"border-radius: 15%;")
        self.camara.threadFlagScan.set()
        # self.camara.scanning = True

        # self.ui.pushButtonFoto.setEnabled(False)
        # self.ui.pushButtonValvula.setEnabled(False)
        # self.ui.pushButtonIluminacion.setEnabled(False)
        # self.ui.pushButtonComando.setEnabled(False)
        # self.ui.lineEditDireccion.setEnabled(False)
        # self.ui.lineEditDistancia.setEnabled(False)
    
        # self.driver.rodillosAction()  #----COMUNICACION----
        # self.driver.osciladorAction()  #----COMUNICACION----


    def enviar(self):
        
        print('ENVIARRR...')
        # self.reading.clear()
        #print(self.reading.is_set())
        time.sleep(2)
        #self.communication.reset_input_buffer()
        #self.communication.reset_output_buffer()
        distancia = self.ui.lineEditDistancia.text()
        direccion = self.ui.lineEditDireccion.text()
        self.driver.move(direccion,distancia)

        
    def pruebas(self):

        if self.modoPruebas is False:
            self.modoPruebas = True
            self.ui.labelPrueba.setText("ON")
            self.ui.pushButtonFoto.setEnabled(True)
            self.ui.pushButtonValvula.setEnabled(True)
            self.ui.pushButtonComando.setEnabled(True)
            self.ui.lineEditDireccion.setEnabled(True)
            self.ui.lineEditDistancia.setEnabled(True)
        else:
            self.modoPruebas = False
            self.ui.labelPrueba.setText("OFF")
            self.ui.pushButtonFoto.setEnabled(False)
            self.ui.pushButtonValvula.setEnabled(False)
            self.ui.pushButtonComando.setEnabled(False)
            self.ui.lineEditDireccion.setEnabled(False)
            self.ui.lineEditDistancia.setEnabled(False)


    def closeEvent(self,event):

        try:
            
            self.camara.stop()
            # self.camara.threadFlagScan.clear()
            self.hiloCamara.join()
            # time.sleep(1)
            # print("cerre hilo camara")
            # self.driver.communication.close()  #----COMUNICACION----
            cv2.destroyAllWindows()
            print('*******Finalizado*******')
        except Exception as e:
            print(f"ERROR AL FINALIZAR: {e}")
    
    

    # def closeEvent(self,event): 

    #     try:
    #         self.isRun = False
    #         self.communication.close()
    #         self.hilo1.join(0.1)
    #         print('*******Finalizado*******')
    #     except Exception as e:
    #         print(e)


    # def recibir(self):
        
    #     while self.isRun:
            
    #         #print(f'maricaaaa!! {self.reading.is_set()}')
    #         if self.reading.is_set() == True:
    #             try:
    #                 #self.communication.reset_input_buffer()
    #                 str = self.communication.readline().decode('utf-8').strip()
                    
    #                 if str:
    #                     try:
    #                         pos = str.index(':')
    #                         label = str[:pos]
    #                         value = str[pos+1:]
    #                         if label == 'VEL':
    #                             self.ui.labelVelocidad.setText(value)
    #                         else:
    #                             continue
    #                     except:
    #                         print('Comando invalido')
    #             except:
    #                 print('hubo un leve error')
    #         else:
    #             continue