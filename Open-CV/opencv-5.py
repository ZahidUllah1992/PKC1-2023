import numpy as np
import cv2 as cv
from cv2 import cvtColor
from cv2 import imshow
from cv2 import imwrite


img = cv.imread('Resources/has.jpg')
img = cv.resize(img, (800, 600))

gray_img = cvtColor(img, cv.COLOR_BGR2GRAY)

imwrite('Hasan_Gray.jpg', gray_img)

#cv.imshow('Hasan', img)
#cv.imshow('Hasan_gray', gray_img)
#cv.imshow('Hasan B&W', binary)
#cv.waitKey(0) 

#cv.destroyAllWindows()

 