import sys
from PyQt5 import QtWidgets
import cv2
import numpy as np
def window():
    app = QtWidgets.QApplication(sys.argv)
    w= QtWidgets.QWidget()
    button1 = QtWidgets.QPushButton(w)
    button2 = QtWidgets.QPushButton(w)
    button1.setText('Click 1')
    button2.setText('Click 2')
    button2.move(100,0)
    w.setWindowTitle('Interface')
    w.setGeometry(0,0,1500,950)
    w.show()
    button1.clicked.connect(on_button1_clicked)
    button2.clicked.connect(on_button2_clicked)
    sys.exit(app.exec_())
def on_button1_clicked():
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame',frame)
            if (cv2.waitKey(25) & 0xFF == ord('q')):
                break
        else:
            break
    cap.release()
def on_button2_clicked():
    cap = cv2.VideoCapture(0)
    ret, last_frame = cap.read()
    if last_frame is None:
        exit()
    while (cap.isOpened()):
        ret, frame = cap.read()
        if frame is None:
            break
        a = cv2.absdiff(last_frame, frame)
        # cv2.imshow('a', a)
        grey = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        # cv2.imshow('gray', blur)
        ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        # cv2.imshow('thre', th)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(th, kernel, iterations=10)
        contours, h = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 5000:
                continue
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(last_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imshow("", last_frame)
        if cv2.waitKey(33) >= 0:
            break
        last_frame = frame
    cap.release()
window()

