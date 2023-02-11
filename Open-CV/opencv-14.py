import numpy as np
import cv2 as cv
#draw canvas

img = np.zeros((600,600))
colored_img = np.zeros((600,600,3), np.uint8)

colored_img[:] = 255,0,255
colored_img[150:230, 100:400] = 255,0,0

cv.line(colored_img, (0,0), (600,230), (255,0,0), 3)

cv.imshow('Hasan', colored_img)
#cv.imshow('Hasan_gray', dilated_img)
#cv.imshow('Hasan B&W', binary)
cv.waitKey(0) 
cv.destroyAllWindows()