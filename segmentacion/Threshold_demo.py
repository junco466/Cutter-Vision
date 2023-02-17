from __future__ import print_function
import cv2 as cv
import argparse





class Calibracion():

    def __init__(self):
        self.max_value = 255
        self.max_type = 4
        self.max_binary_value = 255
        self.trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
        self.trackbar_value = 'Value'
        self.window_name = 'Threshold Demo'


    def Threshold_Demo(self,val):
        #0: Binary
        #1: Binary Inverted
        #2: Threshold Truncated
        #3: Threshold to Zero
        #4: Threshold to Zero Inverted
        threshold_type = cv.getTrackbarPos(self.trackbar_type, self.window_name)
        threshold_value = cv.getTrackbarPos(self.trackbar_value, self.window_name)
        _, dst = cv.threshold(self.src_gray, threshold_value, self.max_binary_value, threshold_type )
        cv.imshow(self.window_name, dst)


    def runCalibracion(self):

        parser = argparse.ArgumentParser(description='Code for Basic Thresholding Operations tutorial.')
        parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
        args = parser.parse_args()
        src = cv.imread("./segmentacion/images/0.png")
        scale = 0.8 # percent of original size
        width = int(src.shape[1] * scale)
        height = int(src.shape[0] * scale)
        dim = (width, height)
        self.src = cv.resize(src, dim, interpolation = cv.INTER_AREA)
        if src is None:
            print('Could not open or find the image: ', args.input)
            exit(0)
        # Convert the image to Gray
        self.src_gray = cv.cvtColor(self.src, cv.COLOR_BGR2GRAY)
        cv.namedWindow(self.window_name)
        cv.createTrackbar(self.trackbar_type, self.window_name , 3, self.max_type, self.Threshold_Demo)
        # Create Trackbar to choose Threshold value
        cv.createTrackbar(self.trackbar_value, self.window_name , 0, self.max_value, self.Threshold_Demo)
        
        # Call the function to initialize
        self.Threshold_Demo(0)
        # Wait until user finishes program
        cv.waitKey()

   
