######################################################################
# Accelerator-gyroscope measurements
######################################################################
#!/usr/bin/env python3
import time
import sched
import threading
import math
from mpu6050 import mpu6050

class Sensor:
	MEASURE_INTERVAL = 0.05

	def __init__(self):
		# sensor setup
		self.sensor = mpu6050(0x68)
		self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
		# necessary entity
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.lock = threading.Lock()
		self.e1 = None
		self.t = None
		# set for calibrating
		self.accel_offset = dict()
		self.accel_offset['x'] = self.accel_offset['y'] = self.accel_offset['z'] = 0
		self.gyro_offset = dict()
		self.gyro_offset['x'] = self.gyro_offset['y'] = self.gyro_offset['z'] = 0
		self.calibrate()
		# data recording
		self.vx = self.vy = 0
		self.dx = self.dy = 0
		self.anglez = 0

	def start_measure(self, measure_interval=None):
		if (measure_interval is None):
			measure_interval = self.MEASURE_INTERVAL

		# start measurements series
		self.e1 = self.scheduler.enter(measure_interval, 1, self.measure)
		self.t = threading.Thread(target=self.scheduler.run)
		self.t.start()

	def end_measure(self):
		# end measurements series and wait for the thread to join
		self.scheduler.cancel(self.e1)
		self.t.join()

	def measure(self, measure_interval):
		if (measure_interval is None):
			measure_interval = self.MEASURE_INTERVAL

		'''
		Perform one measurement and schedule the next
		'''
		self.e1 = self.scheduler.enter(measure_interval, 1, self.measure)
		accel = self.sensor.get_accel_data()
		gyro =  self.sensor.get_gyro_data()
		accel_x = accel['x'] - self.accel_offset['x']
		accel_y = accel['y'] - self.accel_offset['y']
		cosine = math.cos(self.anglez * math.pi / 180.0)
		sine = math.sin(self.anglez * math.pi / 180.0)
		lock.acquire()
		self.vx += accel_x * self.MEASURE_INTERVAL * cosine
		self.vx += accel_y * self.MEASURE_INTERVAL * sine
		self.vy += accel_y * self.MEASURE_INTERVAL * cosine
		self.vy += accel_x * self.MEASURE_INTERVAL * (-sine)
		self.dx += self.vx * self.MEASURE_INTERVAL
		self.dy += self.vy * self.MEASURE_INTERVAL
		self.anglez += (gyro['z'] - self.gyro_offset['z']) * self.MEASURE_INTERVAL
		lock.release()

	def calibrate(self):
		'''
		Calibrate
		'''
		accel = self.sensor.get_accel_data()
		gyro =  self.sensor.get_gyro_data()
		self.accel_offset['x'] = accel['x']
		self.accel_offset['y'] = accel['y']
		self.accel_offset['z'] = accel['z']
		self.gyro_offset['x'] = gyro['x']
		self.gyro_offset['y'] = gyro['y']
		self.gyro_offset['z'] = gyro['z']
		# print("calibrate accel:", self.accel_offset)
		# print("calibrate gyro:", self.gyro_offset)

	def reset(self):
		self.vx = self.vy = 0
		self.dx = self.dy = 0
		self.anglez = 0		

	def get_position(self):
		lock.acquire()
		dx, dy = self.dx, self.dy
		lock.release()
		return dx, dy

	def get_angle(self):
		lock.acquire()
		angle = self.anglez
		lock.release()
		return angle