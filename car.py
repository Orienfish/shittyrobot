######################################################################
# Car module including control
######################################################################
#!/usr/bin/env python3
import time
import threading
from adafruit_motorkit import MotorKit
from sensor import Sensor

class Car:
	# define directions
	FORWARD = 0
	BACKWARD = 1
	LEFT = 2
	RIGHT = 3
	# constant parameters
	STEP = 0.4
	MOVE_INTERVAL = 0.3
	TURN_INTERVAL = 0.1

	def __init__(self):
		# motor setup
		self.rMotor = MotorKit().motor1
		self.lMotor = MotorKit().motor4
		self.sensor = Sensor()

	def Move(self, dir, step=None, move_time=None, turn_time=None):
		'''
		Move the car and trigger measurements
		'''
		if (step is None):
			step = self.STEP
		if (move_time is None):
			move_time = self.MOVE_INTERVAL
		if (turn_time is None):
			turn_time = self.TURN_INTERVAL
		# determine direction
		left, right = 0, 0
		interval = 0
		if (dir == self.FORWARD):
			left, right = 1, 1
			interval = move_time
		elif (dir == self.BACKWARD):
			left, right = -1, -1
			interval = move_time
		elif (dir == self.LEFT):
			left, right = -1, 1
			interval = turn_time
		elif (dir == self.RIGHT):
			left, right = 1, -1
			interval = turn_time
		else:
			return
		
		self.sensor.reset()
		self.sensor.start_measure()

		# move the car forward
		# self.lock.acquire()
		self.rMotor.throttle, self.lMotor.throttle = right*step, left*step
		# self.lock.release()
		time.sleep(interval)
		self.rMotor.throttle, self.lMotor.throttle = 0, 0
		time.sleep(0.02)	
		# end measurement
		self.sensor.end_measure()

		dx, dy = self.sensor.get_position()
		angle = self.sensor.get_angle()
		return dx, dy, angle # the incremental distance and angle lists caused by this movement
	
		

def main():
	myCar = Car()
	myCar.Move(myCar.FORWARD, motor_time=1)
	# myCar.Move(myCar.RIGHT)
	#time.sleep(0.4)


if __name__ == '__main__':
	main()
