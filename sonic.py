######################################################################
# Ultrasonic distance sensor
######################################################################
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class Sonic:
    TRIG = 18
    ECHO = 27
    TIME_OUT = 300
    MEASURE_CNT = 10
    THRESHOLD = 1000.0

    def __init__(self):
        # set up sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False) # init to false
        self.distance = 0

    def one_measure(self):
        '''
        trigger and measure, return with cm
        '''
        # trigger
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001) # last 1ns to trigger
        GPIO.output(self.TRIG, False)
        # measure
        pulse_start, pulse_stop = None, None
        count = 0
        while GPIO.input(self.ECHO) == 0:
            if count >= self.TIME_OUT:
                return 2000
            pulse_start = time.time()
            count += 1
        count = 0
        while GPIO.input(self.ECHO) == 1:
            if count >= self.TIME_OUT:
                return 2000
            pulse_stop = time.time()
            count += 1
        if not pulse_stop or not pulse_start:
            return 2000
        pulse_duration = pulse_stop - pulse_start
        self.distance = round(pulse_duration * 17150, 2)
        return self.distance

    def step_measure(self, measure_cnt = None, threshold = None):
        '''
        make a seris of sonic measurements
        '''
        if (measure_cnt == None):
            measure_cnt = self.MEASURE_CNT
        if (threshold == None):
            threshold = self.THRESHOLD
        average = 0
        count = 0
        for i in range(measure_cnt):
            val = self.one_measure()
            if val > threshold: # do not count outliers
                continue
            average += val
            print(val)
            count += 1
        depth = None
        if count > 0:
            depth = average / count 
        return depth

    def get_distance(self):
        return self.distance

def main():
    sonic = Sonic()
    while (1):
        print("distance:", sonic.measure(), "cm")

if __name__ == '__main__':
    main()
