# Shittyrobot 
A Remote-Controlled Robot Vehicle for 2-D Map Reconstruction. Built in UCSD CSE237A, based on Raspberry Pi 3B+.
Collaborator: [Michael Liu](https://github.com/iosmichael). 
<div align=left><img width="300" height="275" src="https://github.com/Orienfish/Shittyrobot/blob/master/img/car_final.jpg"/></div>
This tutorial will walk you through how to build a robot vehicle from scratch, and share some of our experiences.

## Introduction
Indoor map reconstruction is the first step for any location-based services. In this project, we tried to build a robot vehicle which travels around the room under remote control and measures distance with stereo camera and ultrasonic sensor. We select stereo camera because it contains high dimensional information thus is theoretically more suitable for environment reconstruction. Ultrasonic sensor is used to compensate when stereo camera doesn't work well - when there's a wall locating closely in front of the robot.

However, to be honest, the final system does not perform well. An important lesson I learned here is: **sensor selection is the first and foremost step in embedded system implementation!** Here are the possible reasons and my **suggestions** if you plan to work on similar projects:
* Cheap stereo cameras (ELP Dual Lens Camera) are hard to calibrate and generate poor disparity maps. If you have enough budget, I would recommend using [Intel's RealSense Camera](https://realsense.intel.com/) or depth camera. Their well-developed tools will not only save your time but give you better output.
* Cheap ultrasonic sensors (HC-SR04) perform poorly. They are good if you want to detect a wall with a distance less than 1m (although the standard range is 4m, it does not perform stablely when the distance is larger than 1m). However, the signals may bounce around in the room thus perform badly in a more complex environment, e.g. trying to detect a box. What's more, bear in mind that multiple ultrasonic sensors or multiple emissions may interfere with each other, too. If you insist on these distance-based sensors, I would suggest using the more promising [LiDAR sensor](https://irlock.com/products/tfmini-rangefinder?variant=15818579050547&utm_campaign=gs-2018-09-19&utm_source=google&utm_medium=smart_campaign&gclid=Cj0KCQiAtvPjBRDPARIsAJfZz0qQhvE5Wgyua1VzXPhsCDu_GOqgUyapprkPiMQiIYT7c_cRWPb5QysaAt5BEALw_wcB).

## Hardware List
* Adafruit (PID 3244) Mini 3-Layer Round Robot Chassis Kit - 2WD with DC Motors. [Link](https://www.adafruit.com/product/3244)
* Adafruit DC & Stepper Motor HAT for Raspberry Pi - Mini Kit. [Link](https://www.adafruit.com/product/2348)
* 4 * 1.5V AA Battery Case Holder. [Link](https://www.amazon.com/gp/product/B075G8XZLM/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
* MPU-6050 3-Axis Accelerometer and Gyroscope, using I2C/SPI. [Link](https://www.amazon.com/gp/product/B008BOPN40/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1)
* HC-SR04 Ultrasonic Sensor. [Link](https://www.adafruit.com/product/3942)
* ELP Dual Lens Stereo Camera. ELP-960P2CAM-V90-VC. [Link](https://www.amazon.com/ELP-Industrial-Application-Synchronized-ELP-960P2CAM-V90-VC/dp/B078TDLHCP/ref=cm_cr_arp_d_product_top?ie=UTF8)

## Software List
* Qt for Python (qt-dev, vis.py).
* Stereo camera calibration and depth calculations (stereo).
* Adafruit motor kit driver (car.py). 
* A path tracking module based on mpu6050 (sensor.py)
* A distance detection module based on HC-SR04 (sonic.py)

## How to assemble a robot vehicle from scratch
1. Assemble robot kit and drive motors. This could be quickly done by following Adafruit's wonderful [tutorial](https://learn.adafruit.com/adafruit-motor-shield-v2-for-arduino/overview)
<div align=left><img width="1000" height="250" src="https://github.com/Orienfish/Shittyrobot/blob/master/img/assemble.png"/></div>
2. Connect MPU-6050 to Raspberry Pi through I2C. Then install `python3-smbus` (`python-smbus`) dependencies:

```
sudo apt install python3-smbus
```

Then install `mpu6050-raspberrypi` package from Pypi repository:

```
pip3 install mpu6050-raspberrypi
```

Finally you can get the accelerometer and gyroscope's data by:

```python
from mpu6050 import mpu6050
sensor = mpu6050(0x68)
accelerometer_data = sensor.get_accel_data()
gyroscope_data = sensor.get_gyro_data()
```

Basically, this package can help you read raw data from MPU-6050 and set range. The available range of accelerometer is +-2G, +-4G, +-8G, +-16G while the range gyroscope is +-250, +-500, +-1000, +-2000 degrees per second. It's important to set the proper measurement range. <br>
You can check the [tutorial](https://pypi.org/project/mpu6050-raspberrypi/) for package install. The datasheet of MPU-6050 can be found [here](https://store.invensense.com/datasheets/invensense/MPU-6050_DataSheet_V3%204.pdf).

3. Connect ultrasonic sensor to Raspberry Pi through GPIO. Notice that you need to use extra resistors as the output voltage of ultrasonic sensor is 5V but the maximum acceptable voltage of GPIO is 3.3V.

4. Install OpenCV on Raspberry Pi. <br>
  You can follow this [tutorial](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/) to build an optimized version of OpenCV with NEON and VFPV3 enabled. My experience is that this could improve the speed by around 50%!

## Results