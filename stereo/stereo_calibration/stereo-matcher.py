import sys
import numpy as np
import cv2

REMAP_INTERPOLATION = cv2.INTER_LINEAR

DEPTH_VISUALIZATION_SCALE = 2048

if len(sys.argv) != 2:
    print("Syntax: {0} CALIBRATION_FILE".format(sys.argv[0]))
    sys.exit(1)

calibration = np.load(sys.argv[1], allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])


# TODO: Use more stable identifiers
cap = cv2.VideoCapture(1)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# The distortion in the left and right edges prevents a good calibration, so
# discard the edges
def cropHorizontal(image):
    h, w = image.shape[:2]
    return image[:, int(w/6):int(w/6 * 5)]

# TODO: Why these values in particular?
# TODO: Try applying brightness/contrast/gamma adjustments to the images
stereoMatcher = cv2.StereoBM_create()
stereoMatcher.setMinDisparity(-39)
stereoMatcher.setNumDisparities(128)
stereoMatcher.setTextureThreshold(5)
stereoMatcher.setBlockSize(25)
stereoMatcher.setSpeckleRange(30)
stereoMatcher.setSpeckleWindowSize(171);
stereoMatcher.setPreFilterSize(13)
stereoMatcher.setPreFilterCap(31)

# Grab both frames first, then retrieve to minimize latency between cameras
while(True):
    if not cap.grab():
        print("No more frames")
        break

    _, frame = cap.retrieve()
    h, w = frame.shape[:2]
    leftFrame = frame[:, :w//2]
    rightFrame = frame[:, w//2:]
    # leftFrame = cropHorizontal(leftFrame)
    # rightFrame = cropHorizontal(rightFrame)
    leftHeight, leftWidth = leftFrame.shape[:2]
    rightHeight, rightWidth = rightFrame.shape[:2]

    if (leftWidth, leftHeight) != imageSize:
        print("Left camera has different size than the calibration data")
        break

    if (rightWidth, rightHeight) != imageSize:
        print("Right camera has different size than the calibration data")
        break

    fixedLeft = cv2.remap(leftFrame, leftMapX, leftMapY, REMAP_INTERPOLATION)
    fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)

    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)
    depth = stereoMatcher.compute(grayLeft, grayRight)

    cv2.imshow('left', fixedLeft)
    cv2.imshow('right', fixedRight)
    cv2.imshow('depth', depth / DEPTH_VISUALIZATION_SCALE)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()