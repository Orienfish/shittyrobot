######################################################################
# Car module including control
######################################################################
#!/usr/bin/env python3
import time
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
	MOTOR_INTERVAL = 0.6

	def __init__(self):
		# motor setup
		self.rMotor = MotorKit().motor1
		self.lMotor = MotorKit().motor4
		self.sensor = Sensor()

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
		
		self.sensor.reset()
		self.sensor.start_measure()

		# move the car forward
		self.rMotor.throttle, self.lMotor.throttle = right*step, left*step
		time.sleep(motor_time)
		self.rMotor.throttle, self.lMotor.throttle = 0, 0
		
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
