import cv2
import numpy as np
import time
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=10, disp12MaxDiff=0, uniquenessRatio=20, speckleWindowSize=10, speckleRange=1)
stereo.setPreFilterCap(63)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    gray1 = gray[:, :w//2]
    gray2 = gray[:, w//2:]
    disparity = stereo.compute(gray1, gray2).astype(np.float32)
    disparity = disparity[:, 120:]
    disparity[disparity < 0] = 0
    disparity = disparity / 255
    cv2.imshow('depth', disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
