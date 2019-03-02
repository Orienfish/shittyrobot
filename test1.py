import time
from adafruit_motorkit import MotorKit
from mpu6050 import mpu6050


kit = MotorKit()
sensor = mpu6050(0x68)

rMotor = kit.motor3
rMotor.throttle = 1.0
time.sleep(1)
rMotor.throttle = 0


#lMotor = kit.motor4


#while(1):
#	dir = input("Use W,S,A,D to control direction for a step:)")
#	left, right = 0, 0
#	if dir == 'w':
#		left, right = 0.1, 0.1
#	elif dir == 's':
#		left, right = -0.1, -0.1
#	elif dir == 'a':
#		left, right = -0.1, 0.1
#	elif dir == 'd':
#		left, right = 0.1, -0.1
#	else:
#		print ("Wrong input!")
#		continue
#
#	rMotor.throttle = left
#	lMotor.throttle = right
#	time.sleep(0.5)
#	acc = sensor.get_accel_data()
#	gyro = sensor.get_gyro_data()
#	rMotor.throttle = 0
#	lMotor.throttle = 0

#	print("acc:", acc)
#	print("gyro:", gyro)
