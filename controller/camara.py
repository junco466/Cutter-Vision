import cv2
import numpy as np
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from math import floor
from time import sleep

class Camara():

    #--------------->METODO CONSTRUCTOR (CONFIGURACIONES) <---------------

    def __init__(self,ui,driver): #  ----COMUNICACION----

        self.ui = ui
        self.cap = None
        self.driver = driver #  ----COMUNICACION----

        self.inicio = True
        
        self.threadFlagScan = threading.Event()
        # self.threadFlagScan.clear()
        self.hiloScanner = threading.Thread(target=self.startScan)
        self.hiloScanner.start()

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


            # zoom=self.cap.get(cv2.CAP_PROP_ZOOM)
            # print('zoom', zoom)
            # print('height ', h)
            # print('width ', w)
            # scale = 0.8 # percent of original size
            # width = int(self.frame.shape[1] * scale)
            # height = int(self.frame.shape[0] * scale)
            # dim = (width, height)


            # resize image
            self.frame = cv2.rotate(self.frame,rotateCode = cv2.ROTATE_90_CLOCKWISE)
            # self.frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)


            #IMAGEN EN TIEMPO REAL EN LA INTERFAZ
            cv2.waitKey(1)
            frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            self.ui.labelDisplay.setPixmap(QtGui.QPixmap.fromImage(img))            
            



            # #ENFOQUE DE LA MATRIZ DE LA IMAGEN A PROCESAR:
            # height, width = frame.shape[:2]
            # xi = 240
            # yi = height-400 #max530
            # xf = width-240
            # yf = height-70


            # cv2.rectangle(frame, (xi,yi),(xf,yf),(0,255,0),1)
            # # cv2.rectangle(frame, (xi2,yi2),(xf2,yf2),(0,255,0),1)
            # trim = np.zeros((yf-yi, xf-xi, 3), np.uint8)
            # # trimSensor = np.zeros((yf2-yi2, xf2-xi2, 3), np.uint8)
            # trim[:,:,:] = frame[yi:yf,xi:xf,:]
            # # trimSensor[:,:,:] = frame[yi2:yf2,xi2:xf2,:]

            # #print(f'Tamaño del recorte: {trim.shape}')
            # # grayTrim = cv2.cvtColor(trim, cv2.COLOR_BGR2GRAY)
            # # grayTrim = cv2.GaussianBlur(grayTrim, (7, 7), 0)
            
            
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # self.clasificacion(hsv,frame,frame=frame)
            
            
            # if time.time()-self.t1 > 600:
            #     self.stop()
            # else:
            #     print(f'tiempo: {time.time()-self.t1}')

            # if self.modoCalibracion:
            #     self.calibracion(hsv,trim)
            # else:
            #     self.clasificacion(hsv,trim,frame=frame)
            #     # self.sensorMvovimiento(trimSensor)
                

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
                self.img_counter = 0
                self.scanning = False
                self.threadFlagScan.clear()
                self.ui.pushButtonStart.setEnabled(True)
                self.ui.pushButtonStart.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.547, y1:0.983, x2:0.532105, y2:0, stop:0.0684211 rgba(0, 157, 0, 255), stop:1 rgba(185, 244, 158, 255));\n"
                "border-radius: 15%;")
            else: 
                continue


    def take_photo(self):
        
        print('photo')
        img_name = "{}.png".format(self.img_counter)
        cv2.imwrite(img_name, self.frame)
        print("{} written!".format(img_name))
        self.img_counter += 1


    def take_scene():
        pass


    #****Metodo que realiza la segmentacion, y clasificacion del cafe
    def clasificacion(self,hsv,trim,frame):

        self.ui.labelColor.setText(f"H:{self.DatoHSV[0]}, S:{self.DatoHSV[1]}, V:{self.DatoHSV[2]}")
        hsv = cv2.GaussianBlur(hsv,(9,9),0)

        color_calibrado = np.array([self.DatoHSV[0],self.DatoHSV[1],self.DatoHSV[2]],np.uint8)
        color_calibrado_abajo = np.array([0,0,0],np.uint8) #57,36,16
        color_calibrado_arriba = np.array([0,0,0],np.uint8)

        H_arriba = color_calibrado[0] + 6
        H_abajo = color_calibrado[0] - 6

        S_arriba = color_calibrado[1] + 82
        S_abajo = color_calibrado[1] - 82
        
        V_arriba = color_calibrado[2] + 37
        V_abajo = color_calibrado[2] - 37

        if H_abajo < 0:
            color_calibrado_abajo[0] = 0
            color_calibrado_arriba[0] = H_arriba
        elif H_arriba > 179:
            color_calibrado_abajo[0] = H_abajo
            color_calibrado_arriba[0] = 179
        else:
            color_calibrado_abajo[0] = H_abajo
            color_calibrado_arriba[0] = H_arriba


        if S_abajo < 0:
            color_calibrado_abajo[1] = 0
            color_calibrado_arriba[1] = S_arriba
        elif S_arriba > 255:
            color_calibrado_abajo[1] = S_abajo
            color_calibrado_arriba[1] = 255
        else:
            color_calibrado_abajo[1] = S_abajo
            color_calibrado_arriba[1] = S_arriba    


        if V_abajo < 0:
            color_calibrado_abajo[2] = 0
            color_calibrado_arriba[2] = V_arriba
        elif V_arriba > 255:
            color_calibrado_abajo[2] = V_abajo
            color_calibrado_arriba[2] = 255
        else:
            color_calibrado_abajo[2] = V_abajo
            color_calibrado_arriba[2] = V_arriba         
        
        lower_cafee2 = np.array([127, 70, 40])  # Creamos un vector con los valores minimos del limite         #120,70,40
        upper_cafee2 = np.array([160, 125, 120])  # Creamos un vector con los valores maximos del limite      #195,125,120
        
        mask_HSV_cafee_crudo = cv2.inRange(hsv, color_calibrado_abajo, color_calibrado_arriba)
        mask_HSV_cafee_quemado = cv2.inRange(hsv, lower_cafee2, upper_cafee2)  # Creamos una mascara con los rangos a segmentar

        coffee_crudo,_ = cv2.findContours(mask_HSV_cafee_crudo, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        coffee_quemado,_ = cv2.findContours(mask_HSV_cafee_quemado, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        for c in coffee_crudo:
            area = cv2.contourArea(c)
            # print(f'Area del crudo: {area}')
            if area > self.AreaCrudo:
                self.t1 = time.time()
                # self.driver.electrovalvula()  #----COMUNICACION----
                self.crudo=self.crudo+1
                # print(f'cafe crudo: {self.crudo}')
                M = cv2.moments(c)
                if (M["m00"]==0): M["m00"]=1
                x = int(M["m10"]/M["m00"])
                y = int(M['m01']/M['m00'])
                cv2.circle(frame, (x,y), 7, (0,255,0), -1)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)


        for c in coffee_quemado:
            area = cv2.contourArea(c)
            # print(f'Area del quemado: {area}')
            if area > self.AreaQuemado:
                self.t1 = time.time()
                # self.driver.electrovalvula()  #----COMUNICACION----
                self.quemado=self.quemado+1
                # print(f'cafe quemado: {self.quemado}')
                M = cv2.moments(c)
                if (M["m00"]==0): M["m00"]=1
                x = int(M["m10"]/M["m00"])
                y = int(M['m01']/M['m00'])
                cv2.circle(frame, (x,y), 7, (0,255,0), -1)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)


        
        #IMAGEN EN TIEMPO REAL EN LA INTERFAZ
        frame = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
        img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.ui.labelDisplay.setPixmap(QtGui.QPixmap.fromImage(img))


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