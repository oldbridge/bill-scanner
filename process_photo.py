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
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2),x,1)
        self.img_rot = cv2.warpAffine(self.img_orig,M,(self.cols,self.rows))

    def select_crop(self, event,x,y,flags,param):
        global ix, iy, orig_img, crop_rect, new_img
        if event == cv2.EVENT_LBUTTONDOWN:
            ix = x
            iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            self.crop_rect = {'ix':ix, 'iy':iy, 'ex':x, 'ey':y}


    def __init__(self, route):
        self.route = route
        self.img_orig = cv2.imread(self.route)
        self.img = np.copy(self.img_orig)
        self.img_rot = np.copy(self.img_orig)
        self.rows,self.cols, self.colors = self.img_orig.shape
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('trackbars', cv2.WINDOW_NORMAL)
        self.selection = np.zeros((self.rows, self.cols, self.colors),np.int8)
        # create trackbar for rotation
        cv2.createTrackbar('Rotate','trackbars',0,360*60,self.rotate)
        cv2.setMouseCallback('image', self.select_crop)
        self.crop_rect = {'ix':0, 'iy':0, 'ex':0, 'ey':0}
        "Crop and rotate the photo"
        while(1):
            cv2.imshow('image',self.img)
            top = cv2.getTrackbarPos('Top','trackbars')
            bottom = cv2.getTrackbarPos('Bottom','trackbars')
            self.img = np.copy(self.img_rot)
            #selection = np.zeros((rows, cols, colors),np.int8)
            cv2.rectangle(self.img, (self.crop_rect['ix'], self.crop_rect['iy']),
                          (self.crop_rect['ex'], self.crop_rect['ey']), (255,0,0),10)
            k = cv2.waitKey(1) & 0xFF
            if k == 27: # press ESC to abort process
                cv2.destroyAllWindows()
                sys.exit()
            elif k == 32: # press SPACE to accept
                break
        if self.crop_rect['ix'] >= self.crop_rect['ex']:
            aux = self.crop_rect['ex']
            self.crop_rect['ex'] = self.crop_rect['ix']
            self.crop_rect['ix'] = aux
        if self.crop_rect['iy'] >= self.crop_rect['ey']:
            aux = self.crop_rect['iy']
            self.crop_rect['iy'] = self.crop_rect['ey']
            self.crop_rect['ey'] = aux
        self.img_plot = np.zeros((self.crop_rect['ey']-self.crop_rect['iy'], self.crop_rect['ex']-self.crop_rect['ix']),np.uint8)
        self.img_plot = self.img_rot[self.crop_rect['iy']:self.crop_rect['ey'],self.crop_rect['ix']:self.crop_rect['ex'],:]
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


