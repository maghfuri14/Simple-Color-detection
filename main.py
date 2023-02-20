import json
import cv2
import trackbar
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import *

import module

mode = 'calib'
source = cv2.VideoCapture(0)

dataCalib = []


def winodow():  # create Window
    app = QApplication(sys.argv)
    w = QWidget()
    button = QPushButton(w)
    button.setText("Calibration")
    button.clicked.connect(calibration)
    button.move(50, 50)
    runMainProgram = QPushButton(w)
    runMainProgram.setText("Run Program")
    runMainProgram.move(200, 50)

    runMainProgram.clicked.connect(runProgram)
    closeProgram = QPushButton(w)
    closeProgram.setText("Close Program")
    closeProgram.move(350, 50)
    w.setWindowTitle("Choose Action")
    closeProgram.clicked.connect(close)
    w.show()
    sys.exit(app.exec())


def saveCalib():
    global mode, dataCalib
    load = json.load(open("calib.txt"))
    load['warna'] = dataCalib
    json.dump(load, open("calib.txt", 'w'))
    print("warna calibrated")


def resizeImage(src, scale):
    width = int(src.shape[1] * scale / 100)
    height = int(src.shape[0] * scale / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(src, dim, interpolation=cv2.INTER_AREA)
    return resized


def runProgram():
    global mode
    mode = 'main'
    load = json.load(open("calib.txt"))
    list_meja = load['warna']

    while source.isOpened() and mode == 'main':
        _, frame = source.read()
        # frame = cv2.imread('skripsi/banner1.jpg', 1)   # Grab the current frame
        frame = cv2.imread('image4.jpg', 1)
        frame = resizeImage(frame, 60)
        y = frame.shape[0]
        x = frame.shape[1]

        # cv2.imshow("Asli", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        if frame is None:
            break

        warna = module.deteksiWarna(hsv_frame, (list_meja[0], list_meja[1], list_meja[2]),
                                    (list_meja[3], list_meja[4], list_meja[5]))
        # cv2.imshow("mask", warna)
        cntsWarna = module.deteksiObjek(warna)
        cHasil = module.drawImage(frame, cntsWarna)
        x2, y2, w, h = cv2.boundingRect(cntsWarna[0])
        cv2.rectangle(cHasil, (x, y), (x+w, y+h), (0, 0, 0), 2)
        for c in cntsWarna:
            x1, y1 = module.getCenter(c)
            Hx = x-(w/2)
            Hy = y-(h/2)
            print(f"x = {x1}, y = {y1}")
            # print(f"x = {Hx}, y = {Hy}")
            # cv2.circle(cHasil, (x, y), 5, (255, 0, 0), -1)
            # cv2.circle(cHasil, (int(Hx), int(Hy)), 5, (255, 0, 0), -1)
            cv2.circle(cHasil, (x2, y2), 5, (255, 0, 0), -1)
            cv2.line(cHasil, (0, int(Hy)), (x, int(Hy)), (255, 0, 0), 2)
            # cv2.line(
            #     cHasil, (0,  int(y/2)), (x, int(y/2)), (0, 0, 0), 2)
            # get x,y image

        cv2.imshow('hasil', cHasil)
        cv2.waitKey(1)
    cv2.destroyAllWindows()


def close():
    global mode
    mode = "close"


def calibration():
    global mode, dataCalib
    mode = 'calib'

    trackbar.setup('HSV')
    while source.isOpened() and mode == 'calib':
        _, frame = source.read()
        # frame = cv2.imread('skripsi/banner1.jpg', 1)   # Grab the current frame
        frame = cv2.imread('image4.jpg', 1)

        frame = resizeImage(frame, 60)
        y = frame.shape[0]
        x = frame.shape[1]
        cv2.line(
            frame, (0,  int(y/2)), (x, int(y/2)), (255, 0, 255), 2)

        # cv2.imshow("Asli", frame)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        if frame is None:
            break
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = trackbar.get_values(
            "HSV")
        dataCalib = trackbar.get_values(
            "HSV")
        warna = module.deteksiWarna(hsv_frame, (v1_min, v2_min, v3_min),
                                    (v1_max, v2_max, v3_max))
        cv2.imshow("mask", warna)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            saveCalib()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    winodow()
