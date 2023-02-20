import cv2


def coba(data):
    pass

    # for i in ["MIN", "MAX"]:
    #     for j in 'HSV':
    #         v = cv2.getTrackbarPos("%s_%s" % (j, i), "Calibration")
    #         print(v)


def setup(mode):
    cv2.namedWindow("Calibration", cv2.WINDOW_AUTOSIZE)
    for x in ['MIN', 'MAX']:
        v = 0 if x == "MIN" else 255
        for i in mode:
            cv2.createTrackbar('%s_%s' %
                               (i, x), 'Calibration', v, 255, coba)


def get_values(mode):
    values = []
    for i in ["MIN", "MAX"]:
        for j in mode:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Calibration")
            values.append(v)
    return values
