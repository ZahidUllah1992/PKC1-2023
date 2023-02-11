import numpy as np
import cv2 as cv

cap = cv.VideoCapture('Resources/next.mp4')

if (cap.isOpened() == False):
    print('error in reading video,')

while(True):
    (ret, frame) = cap.read()
    grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if ret == True:
        cv.imshow('Video', grayframe)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv.destroyAllWindows()