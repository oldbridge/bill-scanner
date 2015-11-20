import cv2
import numpy as np
import sys

class ProcessPhoto:
    def nothing(self, x):
        pass


    def threshold(self, x):
        "Apply a certain thrshold"
        (thresh, self.img_th) = cv2.threshold(self.img_bw, x, 255, cv2.THRESH_BINARY)


    def rotate(self, x):
        "Rotate the picture 1 tick per minute"
        x = x / 60
        M = cv2.getRotationMatrix2D((cols/2,rows/2),x,1)
        self.img_rot = cv2.warpAffine(self.img_orig,M,(self.cols,self.rows))


    def __init__(self, route):
        self.route = route
        self.img_orig = cv2.imread(self.route)
        self.img = np.copy(self.img_orig)
        self.img_rot = np.copy(self.img_orig)
        self.rows,self.cols, self.colors = self.img_orig.shape
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('trackbars', cv2.WINDOW_NORMAL)
        self.selection = np.zeros((self.rows, self.cols, self.colors),np.int8)
        # create trackbars for cropping & rotation
        cv2.createTrackbar('Rotate','trackbars',0,360*60,self.rotate)
        cv2.createTrackbar('Top', 'trackbars',0,self.rows, self.nothing)
        cv2.createTrackbar('Bottom', 'trackbars',0,self.rows, self.nothing)
        cv2.createTrackbar('Right', 'trackbars',0,self.rows, self.nothing)
        cv2.createTrackbar('Left', 'trackbars',0,self.rows, self.nothing)
    
        "Crop and rotate the photo"
        while(1):
            self.rows, self.cols, self.colors = self.img.shape
            cv2.imshow('image',self.img)
            top = cv2.getTrackbarPos('Top','trackbars')
            bottom = cv2.getTrackbarPos('Bottom','trackbars')
            r = cv2.getTrackbarPos('Right','trackbars')
            l = cv2.getTrackbarPos('Left','trackbars')
            img = np.copy(self.img_rot)
            #selection = np.zeros((rows, cols, colors),np.int8)
            cv2.rectangle(self.img, (l,top),(r, bottom),(255,0,0),10)
            k = cv2.waitKey(1) & 0xFF
            if k == 27: # press ESC to abort process
                cv2.destroyAllWindows()
                sys.exit()
            elif k == 32: # press SPACE to accept
                break
        if l >= r:
            aux = l
            l = r
            r = aux
        if top >= bottom:
            aux = top
            top = bottom
            bottom = aux
        self.img_plot = np.zeros((bottom-top, r-l),np.uint8)
        self.img_plot = self.img_rot[top:bottom,l:r,:]
        self.img_bw = np.zeros((self.rows, self.cols), np.int8)
    
        cv2.destroyWindow('trackbars')
        cv2.namedWindow('trackbars', cv2.WINDOW_NORMAL)
        cv2.createTrackbar('Threshold', 'trackbars',0,255, self.threshold)
    
        self.img_bw = cv2.cvtColor(self.img_plot, cv2.COLOR_BGR2GRAY)
        self.img_th = np.copy(self.img_bw)
    
        "Display the cropped picture only"
        while(1):
            cv2.imshow('image', self.img_th)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()
                sys.exit()
            elif k == 32: # press SPACE to accept
                break
        cv2.imwrite(self.route + '_bw.png', self.img_th)


