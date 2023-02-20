
import cv2
import imutils
from imutils import perspective
import numpy as np
import time
from imutils import contours


def getCenter(c):
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return [cX, cY]


def deteksiWarna(hsv_frame, colorLower, colorUpper):
    kernel = np.ones((3, 3), np.uint8)
    color_mask = cv2.inRange(hsv_frame, colorLower,
                             colorUpper)  # mencari warna
    # morfologi citra (dilatasi -> erosi)

    hasil = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('mask', hasil)
    return hasil


def deteksiObjek(warna):

    # start find contours in the edge map
    cnts = cv2.findContours(warna.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    if len(cnts) > 1:
        (cnts, _) = contours.sort_contours(cnts)

    return cnts


def drawImage(frame, cnts):
    # loop over the contours individually
    orig = frame.copy()
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 1000:
            continue

        # compute the rotated bounding box of the contour
        # crop

        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box

        # compute the center of the contour
        # mencari titik tengah object

        cX, cY = getCenter(c)
        # M = cv2.moments(c)
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        # ini nggak ada merah-merah dipojok
        cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)
        cv2.circle(orig, (cX, cY), 5, (255, 255, 255), -1)
        # cv2.putText(orig, f"object  {cX,cY}", (cX - 20, cY - 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(orig, f"  {cv2.contourArea(c)}", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # akhir mencari titik tengah

        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
        # cv2.imshow('hhh', orig)
    return orig
