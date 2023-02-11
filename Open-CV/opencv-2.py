import numpy as np
import cv2 as cv

img = cv.imread('Resources/has.jpg')
img = cv.resize(img, (800, 600))
cv.imshow('Hasan', img)
cv.waitKey(0)

cv.destroyAllWindows()
