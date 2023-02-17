import numpy as np
import cv2
import os
from skimage.io import imread_collection


def crop_img(img):
    height = img.shape[0]
    width = img.shape[1]

    cut_heigth=400 #Cortar arriba y abajo la mitad de este valor
    x, y = 0, cut_heigth//2

    #img = img[y:y+height, x:x+width]
    img_display=img.copy()#imagen para mostrar a color
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #--------------   THRESHOLD ------------------#
    ret,th1 = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY); 

    #-------------- CONTORNOS CROP----------------#
    contourns, hierarchy=cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    valid_contourns=[]
    len_valid_contourns=[]
    for c in range(len(contourns)):
        if(cv2.contourArea(contourns[c])>3500): #ignorar contornos pequeños
            valid_contourns.append(contourns[c])
            len_valid_contourns.append(cv2.contourArea(contourns[c]))
        else:
            pass
    ind_largest=np.argmax(len_valid_contourns,axis=0)#Indice del contorno mas grande
     
    #Mascara de recorte
    mask = np.zeros_like(th1)
    cv2.drawContours(mask, valid_contourns, ind_largest, 255, -1)

    #Crop
    (y, x) = np.where(mask == 255)
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))

    crop = img_display[topy:bottomy+1, topx:bottomx+1]

    #----------    RESIZE  ----------------------# Para ver completo en monitor
    scale = 0.6 # percent of original size
    width = int(img_display.shape[1] * scale)
    height = int(img_display.shape[0] * scale)
    dim = (width, height)
    img_display = cv2.resize(img_display, dim, interpolation = cv2.INTER_AREA)
    #crop = cv2.resize(crop, dim, interpolation = cv2.INTER_AREA)
    #--------------------------------------------#

    return crop
    # return th1

def segmentar():
    crop_folder = './segmentacion/images/crop_images/*.png'
    crop_images=imread_collection(crop_folder)

    img_counter = 0
    conteo_esquejes=0
    for img in crop_images:
        img_display=img.copy()#imagen para mostrar a color
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #--------------   THRESHOLD ------------------#
        ret,th1 = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY); 

        #-------------- CONTORNOS CROP----------------#
        contourns, hierarchy=cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        valid_contourns=[]

        for c in range(len(contourns)):
            if((cv2.contourArea(contourns[c])>1000) & (cv2.contourArea(contourns[c])<20000)): #ignorar contornos pequeños
                valid_contourns.append(contourns[c])
                #print(cv2.contourArea(contourns[c]))
            else:
                pass
        for c in range(len(valid_contourns)):
            rect=cv2.minAreaRect(valid_contourns[c])
            box=cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img_display,[box],0,(0,255,0),3) 
            cv2.drawContours(img_display,valid_contourns[c],-1,(0,0,255),2)
            #cv2.imshow('contornos',img_display)
            conteo_esquejes+=1
        #cv2.waitKey(0)
        final_img_name = "./segmentacion/images/final_images/{}.png".format(img_counter)

        cv2.imwrite(final_img_name, img_display) #Guardar imagen
        print("{}_final written!".format(img_counter))
        img_counter += 1
    return(conteo_esquejes)


def main_seg():

    images_folder = './segmentacion/images/*.png'
    images=imread_collection(images_folder)
    img_counter = 0
    conteo_esquejes=0
    for img in images:
        img_name = "{}.png".format(img_counter)
        crop_img_name = "./segmentacion/images/crop_images/{}.png".format(img_counter)

        cv2.imwrite(crop_img_name, crop_img(img)) #Guardar imagen
        print("{}_crop written!".format(img_name))

        img_counter += 1
        #cv2.imshow(img_name, crop_img(img)) #Mostrar imagen
    
    #cv2.waitKey(0)
    conteo_esquejes=segmentar()
    print("Conteo: ",conteo_esquejes)
    return conteo_esquejes