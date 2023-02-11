import numpy as np
import cv2 as cv
from cv2 import cvtColor
from cv2 import imshow
from cv2 import imwrite


img = cv.imread('Resources/has.jpg')
img = cv.resize(img, (800, 600))

gray_img = cvtColor(img, cv.COLOR_BGR2GRAY)

blurr_img=cv.GaussianBlur(img, (23,23),0)
edge_img = cv.Canny(img, 48,48)

dilated_img = cv.dilate(edge_img, (7,7), iterations=2)

cropped_img = img[50:350, 300:500]
#imwrite('Hasan_Gray.jpg', gray_img)

cv.imshow('Hasan', cropped_img)
cv.imshow('Hasan_gray', dilated_img)
#cv.imshow('Hasan B&W', binary)
cv.waitKey(0) 
cv.destroyAllWindows()