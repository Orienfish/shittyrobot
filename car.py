######################################################################
# Car module including control and accelerator-gyroscope measurements
######################################################################
#!/usr/bin/env python3
import time
import sched
import threading
import math
from adafruit_motorkit import MotorKit
from mpu6050 import mpu6050

class Car:
	# define directions
	FORWARD = 0
	BACKWARD = 1
	LEFT = 2
	RIGHT = 3
	# constant parameters
	STEP = 0.4
	MEASURE_INTERVAL = 0.05
	MOTOR_INTERVAL = 0.5

	def __init__(self):
		# sensor setup
		self.sensor = mpu6050(0x68)
		self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
		self.rMotor = MotorKit().motor1
		self.lMotor = MotorKit().motor4
		
		# necessary entity
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.lock = threading.Lock()
		self.e1 = None
		# set for calibrating
		self.accel_offset = dict()
		self.accel_offset['x'] = self.accel_offset['y'] = self.accel_offset['z'] = 0
		self.gyro_offset = dict()
		self.gyro_offset['x'] = self.gyro_offset['y'] = self.gyro_offset['z'] = 0
		self.calibrate()
		# data recording
		self.vx = self.vy = 0
		self.dx = self.dy = 0
		# self.velocity = dict()
		# self.velocity['x'] = []
		# self.velocity['y'] = []
		self.distance = dict()
		self.distance['x'] = []
		self.distance['y'] = []
		self.anglez = 0
		self.angle = []

	def Move(self, dir, step=None, motor_time=None):
		'''
		Move the car and trigger measurements
		'''
		if (step is None):
			step = self.STEP
		if (motor_time is None):
			motor_time = self.MOTOR_INTERVAL
		# determine direction
		left, right = 0, 0
		if (dir == self.FORWARD):
			left, right = 1, 1
		elif (dir == self.BACKWARD):
			left, right = -1, -1
		elif (dir == self.LEFT):
			left, right = -1, 1
		elif (dir == self.RIGHT):
			left, right = 1, -1
		else:
			return
		# start measurements series
		self.e1 = self.scheduler.enter(self.MEASURE_INTERVAL, 1, self.measure)
		self.t = threading.Thread(target=self.scheduler.run)
		self.t.start()
		# move the car forward
		self.rMotor.throttle, self.lMotor.throttle = right*step, left*step
		time.sleep(motor_time)
		self.rMotor.throttle, self.lMotor.throttle = 0, 0
		# end measurement
		time.sleep(2*self.MEASURE_INTERVAL) # a gap for complete measurements
		self.scheduler.cancel(self.e1)
		self.t.join()

	def measure(self):
		'''
		Perform one measurement and schedule the next
		'''
		# start = time.time()
		self.e1 = self.scheduler.enter(self.MEASURE_INTERVAL, 1, self.measure)
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
		# print(accel_x, accel_y)
		# print("angle:", self.anglez)
		# print("cos:", cosine, "sin:", sine)
		self.distance['x'].append(self.dx)
		self.distance['y'].append(self.dy)
		self.angle.append(self.anglez)
		# print(time.time() - start)

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

	def reset_velocity(self):
		self.vx = self.vy = 0

	def reset_position(self):
		self.dx = self.dy = 0

	def reset_angle(self):
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
		

def main():
	myCar = Car()
	myCar.Move(myCar.FORWARD, motor_time=1)
	# myCar.Move(myCar.RIGHT)
	#time.sleep(0.4)
	#myCar.Move(myCar.FORWARD, motor_time=1)
	with open("result.txt", "w+") as f:
		f.write(str(myCar.distance['x']) + "\r\n")
		f.write(str(myCar.distance['y']) + "\r\n")
		f.write(str(myCar.angle) + "\r\n")


if __name__ == '__main__':
	main()
