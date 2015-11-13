import cv2
import numpy as np
import sys


def nothing(x):
    pass


def rotate(x):
    "Rotate the picture 1 tick per minute"
    global img_rot, img_orig
    x = x / 60
    M = cv2.getRotationMatrix2D((cols/2,rows/2),x,1)
    img_rot = cv2.warpAffine(img_orig,M,(cols,rows))


# Load the picture of the ticket
img_orig = cv2.imread('ticket.JPG')
img = np.copy(img_orig)
img_rot = np.copy(img_orig)
rows,cols, colors = img_orig.shape
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('trackbars', cv2.WINDOW_NORMAL)
selection = np.zeros((rows, cols, colors),np.int8)
# create trackbars for cropping & rotation
cv2.createTrackbar('Rotate','trackbars',0,360*60,rotate)
cv2.createTrackbar('Top', 'trackbars',0,rows, nothing)
cv2.createTrackbar('Bottom', 'trackbars',0,rows,nothing)
cv2.createTrackbar('Right', 'trackbars',0,rows, nothing)
cv2.createTrackbar('Left', 'trackbars',0,rows, nothing)

"Crop and rotate the photo"
while(1):
    rows,cols, colors = img_orig.shape
    cv2.imshow('image',img)
    top = cv2.getTrackbarPos('Top','trackbars')
    bottom = cv2.getTrackbarPos('Bottom','trackbars')
    r = cv2.getTrackbarPos('Right','trackbars')
    l = cv2.getTrackbarPos('Left','trackbars')
    img = np.copy(img_rot)
    #selection = np.zeros((rows, cols, colors),np.int8)
    cv2.rectangle(img, (l,top),(r, bottom),(255,0,0),10)
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
img_plot = np.zeros((bottom-top, r-l),np.uint8)
img_plot = img_rot[top:bottom,l:r,:]
cv2.destroyWindow('trackbars')

"Display the cropped picture only"
while(1):
    cv2.imshow('image', img_plot)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        sys.exit()