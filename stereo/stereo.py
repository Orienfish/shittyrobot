import cv2
import threading
import math
import numpy as np

class Stereo(object):
    THRESHOLD = 25
    VISUAL_ANGLE = 30
    SCALE = 1 

    def __init__(self, ray):
        self.ray = ray
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def sampling_by_ray(self, disparity_array):
        interval = len(disparity_array) // self.ray
        sampling = []
        index = 0
        for i in range(0, len(disparity_array), interval):
            data = disparity_array[i: i+interval]
            data[np.isinf(data)] = 0
            if len(data[data > 0]) == 0:
                sampling.append(-1)
            else:
                avg = np.mean(data[data>0])
                sampling.append(np.asscalar(avg))    
        print(sampling)
        return sampling
    
    def stereo_read(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]
        gray1 = gray[:, :w//2]
        gray2 = gray[:, w//2:]
        stereo = cv2.StereoSGBM_create(numDisparities=128, blockSize=10, disp12MaxDiff=0, uniquenessRatio=15, speckleWindowSize=131, speckleRange=4)
        disparity = stereo.compute(gray1, gray2).astype(np.float32) / 16 
        depth = 60 * 210 / (320 * disparity)
        depth = depth[h//3: 2 * (h//3), 120:]
        return self.sampling_by_ray(depth)
    
    def stereo_map(self, angle, origin_x, origin_y):
        sampling_data = self.stereo_read()        
        # divide up the visual angles with ray
        interval = self.VISUAL_ANGLE / len(sampling_data)
        print(interval)
        start_angle = angle - self.VISUAL_ANGLE / 2
        xs, ys = [], []
        for i, data in enumerate(sampling_data):
            if data <= 0:
                continue    
            depth = data * self.SCALE
            if depth <= self.THRESHOLD:
                continue
            degree = start_angle + i * interval            
            print('depth: {}'.format(depth))
            degree = degree * math.pi / 180
            x, y = origin_x + depth * math.cos(degree), origin_y + depth * math.sin(degree)
            xs.append(x)
            ys.append(y)
        return xs, ys


