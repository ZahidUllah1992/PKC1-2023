import numpy as np
import cv2 as cv

cap = cv.VideoCapture('Resources/next.mp4')

if (cap.isOpened() == False):
    print('error in reading video,')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv.VideoWriter('Video_Gray.Avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height), isColor=False)
while(True):
    (ret, frame) = cap.read()
    grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if ret == True:
        out.write(grayframe)
        cv.imshow('Video', grayframe)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv.destroyAllWindows()