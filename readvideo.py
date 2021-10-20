import cv2

import numpy as np

cap = cv2.VideoCapture('Bai Tap luyen thu nang cao trong cau long.mp4')
#fps=cap.get(cv2.CAP_PROP_FPS)
#wait_time=1000/fps
ret,last_frame=cap.read()


if last_frame is None:
    exit()
while (cap.isOpened()):
    ret, frame = cap.read()

    if frame is None:
        break

    a = cv2.absdiff(last_frame, frame)

    cv2.imshow('a', a)
    grey = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    cv2.imshow('gray',blur)
    ret, th = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)
    cv2.imshow('thre',th)
    kernel=np.ones((3,3),np.uint8)
    dilated = cv2.dilate(th,kernel, iterations=3)
    contours, h = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt)<5000:
            continue
        (x,y,w,h)=cv2.boundingRect(cnt)
        cv2.rectangle(last_frame,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.imshow("inter",last_frame)
    if cv2.waitKey(33) >= 0:
        break
    last_frame = frame

cap.release()
cv2.destroyAllWindows()

