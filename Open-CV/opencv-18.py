import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)



def hd_resolution():
    cap.set(4,720)
    cap.set(3,1280)

hd_resolution()


frame_width = int(cap.get(4))
frame_height = int(cap.get(3))

out = cv.VideoWriter('Resources/Cam_Video.Avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height), isColor=True)
while(True):
    (ret, frame) = cap.read()
    if ret == True:
        out.write(frame)
        cv.imshow('Video', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv.destroyAllWindows()