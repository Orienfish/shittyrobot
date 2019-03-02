import numpy as np
import cv2

LEFT_PATH = "capture/left/{:04d}.jpg"
RIGHT_PATH = "capture/right/{:04d}.jpg"

CHESSBOARD_SIZE = (9, 6)

MAX_IMAGE = 164

# TODO: Use more stable identifiers
cap = cv2.VideoCapture(1)


# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# The distortion in the left and right edges prevents a good calibration, so
# discard the edges
def cropHorizontal(image):
    h, w = image.shape[:2]
    return image[:, int(w/6):int(w/6 * 5)]

frameId = 100

h, w = 0, 0

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not cap.grab():
        print("No frames")
        break

    if frameId >= MAX_IMAGE:
        break

    _, frame = cap.retrieve()
    h, w = frame.shape[:2]
    leftFrame = frame[:, :w//2]
    rightFrame = frame[:, w//2:]
    leftFrame = cropHorizontal(leftFrame)
    rightFrame = cropHorizontal(rightFrame)
    ret_left, _ = cv2.findChessboardCorners(leftFrame, CHESSBOARD_SIZE, None)
    ret_right, _ = cv2.findChessboardCorners(rightFrame, CHESSBOARD_SIZE, None)
    if ret_left and ret_right:
        cv2.imwrite(LEFT_PATH.format(frameId), leftFrame)
        cv2.imwrite(RIGHT_PATH.format(frameId), rightFrame)
        print('image resolution: {}x{}'.format(h, w//2))
        print('saved image 1 to {}'.format(LEFT_PATH.format(frameId)))
        print('saved image 2 to {}'.format(RIGHT_PATH.format(frameId)))
        frameId += 1

    # cv2.imshow('left', leftFrame)
    # cv2.imshow('right', rightFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()