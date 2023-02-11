import numpy as np
import cv2 as cv

cap = cv.VideoCapture('Resources/next.mp4')

if (cap.isOpened() == False):
    print('error in reading video,')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv.imshow('Video', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv.destroyAllWindows()