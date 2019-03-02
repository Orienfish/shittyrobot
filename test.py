import time
import sched
import threading
from adafruit_motorkit import MotorKit
from mpu6050 import mpu6050

scheduler = sched.scheduler(time.time, time.sleep)
lock = threading.Lock()

# parameters setting
STEP = 0.4
MEASURE_INTERVAL = 0.2
MOTOR_INTERVAL = 0.5

# sensor setup
kit = MotorKit()
sensor = mpu6050(0x68)
sensor.set_accel_range(sensor.ACCEL_RANGE_8G)
print("Accel:", sensor.read_accel_range())
print("Gyro:", sensor.read_gyro_range())
rMotor = kit.motor1
lMotor = kit.motor4

# data recording
accel_x = []
accel_y = []
accel_z = []
gyro_x = []
gyro_y = []
gyro_z = []
e1 = None

def measure():
	global accel_l, gyro_l, e1
	start = time.time()
	e1 = scheduler.enter(MEASURE_INTERVAL, 1, measure)
	accel = sensor.get_accel_data()
	gyro =  sensor.get_gyro_data()
	lock.acquire()
	# print("Time:", start, "acc:", accel, "gyro:", gyro)
	accel_x.append(accel['x'])
	accel_y.append(accel['y'])
	accel_z.append(accel['z'])
	gyro_x.append(gyro['x'])
	gyro_y.append(gyro['y'])
	gyro_z.append(gyro['z'])
	lock.release()

e1 = scheduler.enter(MEASURE_INTERVAL, 1, measure)
t = threading.Thread(target=scheduler.run)
t.start()

left, right = STEP, STEP
for i in range(0, 5):
	# dir = input("Use W,S,A,D to control direction for a step:)")
	#left, right = 0, 0
	#if dir == 'w':
	#	left, right = STEP, STEP
	#elif dir == 's':
	#	left, right = -STEP, -STEP
	#elif dir == 'a':
	#	left, right = -STEP, STEP
	#elif dir == 'd':
	#	left, right = STEP, -STEP
	#else:
	#	print ("Wrong input!")
	#	continue

	left, right = -left, -right
	rMotor.throttle, lMotor.throttle = left, right
	time.sleep(MOTOR_INTERVAL)
	rMotor.throttle, lMotor.throttle = 0, 0
	time.sleep(MOTOR_INTERVAL)

scheduler.cancel(e1)
t.join()

print(accel_x)
print(accel_y)
print(accel_z)
print(gyro_x)
print(gyro_y)
print(gyro_z)
