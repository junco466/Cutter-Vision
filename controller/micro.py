import serial
import time

class Micro():

    def __init__(self,ui):

        #--------------->METODO CONSTRUCTOR (CONFIGURACIONES) <---------------
        
        self.communication = serial.Serial("COM12",9600)
        self.led = True
        self.osc = False
        self.rod = False
        self.ui = ui


#-----------------------------------------------------------------------------------------------------------------------------------

    #--------------->Metodos del controlador del micro y comunicacion<---------------

    def move(self,direccion,distancia):
        #variables = {'posicion' : self.ui.lineEditPosicion.text(),'tixempo' : self.ui.lineEditTiempo.text(), 'direccion' : self.ui.lineEditDireccion.text()}
        #jsonData = json.dumps(variables)

        str = "MOVE:" + direccion + ";" + distancia + "/"
        try:
            self.communication.write(str.encode('ascii'))
            print('envie informacion')
            time.sleep(2)
            # self.reading.set()
            #print(self.reading.is_set())
        except:
            print('error buffer')
            # self.reading.set()


    def home(self):

        str = "HOME/"
        try:
            self.communication.write(str.encode('ascii'))
            print('envie home')
            # time.sleep(2)
        except:
            print('error buffer home')





    # #****Controla la ilimincion LED****
    # def ledAction(self):

    #     if self.led == False:
    #         self.led = True
    #         #self.communication.write("A".encode('utf_8'))            
    #         self.communication.write(b'1')
    #         self.ui.labelIluminacion.setText("ON")
    #     else:
    #         self.led = False
    #         self.communication.write(b'0')
    #         self.ui.labelIluminacion.setText("OFF")
    

    # #****Controla las acciones del oscilador****
    # def osciladorAction(self):

    #     if self.osc == False:
    #         self.osc = True
    #         self.communication.write(b'2')
    #         self.ui.labelOscilador.setText("ON")
    #     else:
    #         self.osc = False
    #         self.communication.write(b'3')
    #         self.ui.labelOscilador.setText("OFF")


    # #****Controla las acciones de los rodillos****
    # def rodillosAction(self):

    #     if self.rod == False:
    #         self.rod = True
    #         self.communication.write(b'4')
    #         self.ui.labelRodillos.setText("ON")
    #     else:
    #         self.rod = False
    #         self.communication.write(b'5')
    #         self.ui.labelRodillos.setText("OFF")

  
    # #****Controla la activacion de la electrovalvula****
    # def electrovalvula(self):
    #     self.communication.write(b'6')


    # #****Controla el cambio de la variable de velocidad en el microcontrolador****
    # def velAction(self,str1):

    #     #Default de valcidad 35 ms
    #     try:
    #         validar = int(str1)
    #         if validar > 500:
    #             str1 = '500'
    #         elif validar < 10:
    #             str1 = '10'

    #         # print(f'este es str1 {str1}')
    #         self.communication.write(b'7')
    #         time.sleep(0.2)
    #         self.communication.write(str1.encode('ascii'))
    #     except:
    #         print('El dato de velocidad debe ser un numero')
