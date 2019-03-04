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
	MEASURE_INTERVAL = 0.04
	CALIBRATE = 10

	def __init__(self):
		# sensor setup
		self.sensor = mpu6050(0x68)
		self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
		# necessary entity
		self.scheduler = sched.scheduler(time.time, time.sleep)
		# self.lock = threading.Lock()
		self.e1 = None
		self.t = None
		# set for calibrating
		self.accel_offset = dict()
		self.accel_offset['x'] = 0.0
		self.accel_offset['y'] = 0.0
		self.accel_offset['z'] = 0.0
		self.gyro_offset = dict()
		self.gyro_offset['x'] = 0.0
		self.gyro_offset['y'] = 0.0
		self.gyro_offset['z'] = 0.0
		self.calibrate()
		# data recording
		self.vx = 0.0
		self.vy = 0.0
		self.dx = 0.0
		self.dy = 0.0
		self.anglez = 0.0

	def start_measure(self):
		# start measurements series
		self.e1 = self.scheduler.enter(self.MEASURE_INTERVAL, 1, self.measure)
		self.t = threading.Thread(target=self.scheduler.run)
		self.t.start()

	def end_measure(self):
		# end measurements series and wait for the thread to join
		self.scheduler.cancel(self.e1)
		self.t.join()

	def measure(self):
		'''
		Perform one measurement and schedule the next  
		'''
		# print("time:", time.time())
		self.e1 = self.scheduler.enter(self.MEASURE_INTERVAL, 1, self.measure)
		accel = self.sensor.get_accel_data()
		gyro =  self.sensor.get_gyro_data()			
		accel_x = accel['x'] - self.accel_offset['x']
		accel_y = accel['y'] - self.accel_offset['y']
		cosine = math.cos(self.anglez * math.pi / 180.0)
		sine = math.sin(self.anglez * math.pi / 180.0)
		# self.lock.acquire()
		self.vx += accel_x * self.MEASURE_INTERVAL * cosine
		self.vx += accel_y * self.MEASURE_INTERVAL * (-sine)
		self.vy += accel_y * self.MEASURE_INTERVAL * cosine
		self.vy += accel_x * self.MEASURE_INTERVAL * sine
		self.dx += self.vx * self.MEASURE_INTERVAL
		self.dy += self.vy * self.MEASURE_INTERVAL      
		self.anglez += (gyro['z'] - self.gyro_offset['z']) * self.MEASURE_INTERVAL

		# self.lock.release()
		# print("ax:", accel_x, "ay:", accel_y)
		# print("dx:", self.dx, "dy:", self.dy, "angle:", self.anglez, "vx:", self.vx, "vy:", self.vy)

	def calibrate(self):
		'''
		Calibrate
		'''
		accel_x = 0.0
		accel_y = 0.0
		accel_z = 0.0
		gyro_x = 0.0
		gyro_y = 0.0
		gyro_z = 0.0
		for i in range(0, self.CALIBRATE):
			accel = self.sensor.get_accel_data()
			gyro =  self.sensor.get_gyro_data()
			accel_x += accel['x']
			accel_y += accel['y']
			accel_z += accel['z']
			gyro_x += gyro['x']
			gyro_y += gyro['y']
			gyro_z += gyro['z']
			# print(accel, gyro)
		self.accel_offset['x'] = accel_x / self.CALIBRATE
		self.accel_offset['y'] = accel_y / self.CALIBRATE
		self.accel_offset['z'] = accel_z / self.CALIBRATE
		self.gyro_offset['x'] = gyro_x / self.CALIBRATE
		self.gyro_offset['y'] = gyro_y / self.CALIBRATE
		self.gyro_offset['z'] = gyro_z / self.CALIBRATE
		# print("calibrate accel:", self.accel_offset)
		# print("calibrate gyro:", self.gyro_offset)

	def reset(self):
		self.vx = 0.0
		self.vy = 0.0
		self.dx = 0.0
		self.dy = 0.0
		self.anglez = 0.0		

	def get_position(self):
		return self.dx, self.dy

	def get_angle(self):
		return self.anglez