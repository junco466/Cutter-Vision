import cv2
import numpy as np
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from View.interfaceFotos import Ui_Presentacion
from segmentacion.seg_main import main_seg
import threading
from math import floor
from time import sleep

class Camara():

    #--------------->METODO CONSTRUCTOR (CONFIGURACIONES) <---------------

    def __init__(self,ui,driver): #  ----COMUNICACION----

        self.ui = ui
        self.cap = None
        self.driver = driver #  ----COMUNICACION----
        self.ventana = QtWidgets.QMainWindow()
        self.ui2 = Ui_Presentacion()
        self.ui2.setupUi(self.ventana)


        self.inicio = True
        
        self.threadFlagScan = threading.Event()
        # self.threadFlagScan.clear()
        self.hiloScanner = threading.Thread(target=self.startScan)
        self.hiloScanner.start()

        self.conteoEsquejes = 0


        self.DatoHSVStandard = [10,173,217] 
        self.DatoHSV = [10,173,217]  #57,36,16
        self.crudo=0
        self.quemado=0
        self.AreaCrudo = 0 #Dato calibrados por Asimov: 900
        self.AreaQuemado = 0 #Dato calibrados por Asimov: 2800
        self.t1 = None
        self.img_counter = 0
        parar = False


#-----------------------------------------------------------------------------------------------------------------------------------


    #--------------->Metodos del controlador de la camara<---------------


    #****Metodo que pone en MAIN de la clase marcha y sostiene la deteccion y clasificacion del cafe****
    def startCamara(self):

        self.t1 = time.time()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_ZOOM,27)


        while self.cap.isOpened():
            
            success, self.frame = self.cap.read()

            #Verificar la conexion de la camara
            if success==False:
                print("play finished")  # Determine la finalización de la reproducción del archivo local
                break

            h = self.frame.shape[0]
            w = self.frame.shape[1]

            # resize image
            self.frame = cv2.rotate(self.frame,rotateCode = cv2.ROTATE_90_CLOCKWISE)
            # self.frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)


            #IMAGEN EN TIEMPO REAL EN LA INTERFAZ
            cv2.waitKey(1)
            frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            self.ui.labelDisplay.setPixmap(QtGui.QPixmap.fromImage(img))            
            
                
    def startScan(self):
        
        while self.inicio:

            if self.threadFlagScan.is_set() == True:

                #>>>>---INICIO DE SACANEO-------<<<<<
                self.driver.home()
                sleep(4)
                self.take_photo()
                self.driver.move("1","290")
                sleep(4)
                self.take_photo()
                self.driver.move("1","290")
                sleep(4)
                self.take_photo()
                self.driver.home()
                sleep(9)

                self.conteoEsquejes = main_seg()

                print('conteo: ', self.conteoEsquejes)
                self.img_counter = 0
                self.scanning = False
                self.threadFlagScan.clear()
                self.ui.labelConteo.setText(str(self.conteoEsquejes))
                self.ui.pushButtonStart.setEnabled(True)
                self.ui.pushButtonStart.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.547, y1:0.983, x2:0.532105, y2:0, stop:0.0684211 rgba(0, 157, 0, 255), stop:1 rgba(185, 244, 158, 255));\n"
                "border-radius: 15%;")
            else: 
                continue


    def take_photo(self):
        
        print('photo')
        img_name = "./segmentacion/images/{}.png".format(self.img_counter)
        cv2.imwrite(img_name, self.frame)
        print("{} written!".format(img_name))
        self.img_counter += 1


    #>>>>-----Definicion Ventana secundaria-----<<<<<
    def fotoWindow(self):

        img0 = QtGui.QPixmap('./segmentacion/images/final_images/0.png')
        img1 = QtGui.QPixmap('./segmentacion/images/final_images/1.png')
        img2 = QtGui.QPixmap('./segmentacion/images/final_images/2.png')

        self.ui2.labelImg0.setPixmap(img0) 
        self.ui2.labelImg1.setPixmap(img1) 
        self.ui2.labelImg2.setPixmap(img2) 
        
        self.ventana.show()


    #****Metodo que detiene el proceso de captura de imagenes, y desactiva dispositivos, luego del cierre****
    def stop(self):

        self.threadFlagScan.clear()
        self.inicio = False
        # sleep(1)
        # print('falso scanning')
        self.hiloScanner.join()
        # sleep(1)
        # print('cerre hilo scanner')
        self.cap.release()
        self.ui.labelDisplay.clear()


#-----------------------------------------------------------------------------------------------------------------------------------