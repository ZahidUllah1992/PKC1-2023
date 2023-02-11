import cv2 as cv

cap = cv.VideoCapture('Resources/next.mp4')

frameNB = 0

while (True):
    success, frame = cap.read()
    if success:
        cv.imwrite(f'Resources/video images/Frams_{frameNB}.jpg', frame)
    else:
        break
    frameNB = frameNB+1

cap.release()