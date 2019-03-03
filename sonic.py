######################################################################
# Ultrasonic distance sensor
######################################################################
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class Sonic:
	TRIG = 1
	ECHO = 2

	def __init__(self):
		# set up sensor
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False) # init to false
		self.distance = 0

	def measure(self):
		'''
		trigger and measure, return with cm
		'''
		# trigger
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001) # last 1ns to trigger
		GPIO.output(self.TRIG, False)
		# measure
		while GPIO.input(self.ECHO) == 0:
  			pulse_start = time.time()
  		while GPIO.input(self.ECHO) == 1:
  			pulse_stop = time.time()
		pulse_duration = pulse_stop - pulse_start
		self.distance = round(pulse_duration * 17150, 2)
		return self.distance

	def get_distance(self):
		return self.distance

def main():
	sonic = Sonic()
	while (1):
		print("distance:", sonic.measure(), "cm")

if __name__ == '__main__':
	main()