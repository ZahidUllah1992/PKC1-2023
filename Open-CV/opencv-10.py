import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        #out.write(grayframe)
        cv.imshow('Frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'): 
            break
    else:
        break


cap.release()
#out.release()
cv.destroyAllWindows() 