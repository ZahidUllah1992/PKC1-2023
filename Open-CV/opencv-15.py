import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

def hd_resolution():
    cap.set(4,720)
    cap.set(3,1280)

hd_resolution()

while(True):
    (ret, frame) = cap.read()
    if ret == True:
        cv.imshow('Frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
#out.release()
cv.destroyAllWindows()