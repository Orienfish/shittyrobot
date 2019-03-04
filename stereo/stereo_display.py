import cv2
import threading
import math
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    start = time.time()
    ret, frame = cap.read()
    finish_read = time.time()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    gray1 = gray[:, :w//2]
    gray2 = gray[:, w//2:]
    stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=10, disp12MaxDiff=0, uniquenessRatio=15, speckleWindowSize=131, speckleRange=4)
    disparity = stereo.compute(gray1, gray2).astype(np.float32) / 2048
    disparity = disparity[h//3: 2 * (h//3), 120:]
    finish_compute = time.time()
    cv2.imshow('depth', disparity)
    finish_display = time.time()
    print("read time:", finish_read-start, \
          "computation time:", finish_compute-finish_read, \
          "display time:", finish_display-finish_compute)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
