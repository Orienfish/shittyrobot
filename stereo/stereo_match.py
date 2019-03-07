import cv2
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
stereo = cv2.StereoSGBM_create(numDisparities = 128, 
        blockSize = 10,
        disp12MaxDiff = 0,
        uniquenessRatio = 20,
        speckleWindowSize = 10,
        speckleRange = 1
    )
stereo.setPreFilterCap(63)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[0], gray.shape[1]
    gray1 = gray[:, :w//2]
    gray2 = gray[:, w//2:]
    average = None
    for j in range(5):
        disparity = stereo.compute(gray1,gray2).astype(np.float32)
        if j == 0:
            average = disparity
        else:
            average += disparity
    # norm_eff = 255 / disparity.max()
    disparity = average / 10
    disparity[disparity < 0] = 0
    disparity = disparity / 255
    disparity[disparity > 3.7] = 0
    print(disparity.mean(axis=0) + disparity.std(axis=0))
    depth = 4 * 320 / (disparity + 0.1)

    cv2.imshow('depth', disparity)
    cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)
cap.release()