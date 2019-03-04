# Shittyrobot 
A Remote-Controlled Robot Vehicle for 2-D Map Reconstruction. Built in UCSD CSE237A, based on Raspberry Pi 3B+.
Collaborator: [Micheal Liu](https://github.com/iosmichael). 
<div align=center><img width="300" height="300" src="https://github.com/Orienfish/Shittyrobot/blob/master/img/car_final.jpg"/></div>

## Introduction
Indoor map reconstruction is the first step for any location-based services. In this project, we tried to build a robot vehicle which travels around the room under remote control and measures distance with stereo camera and ultrasonic sensor. We select stereo camera because it contains high dimensional information thus is theoretically more suitable for environment reconstruction. Ultrasonic sensor is used to compensate when stereo camera doesn't work well - when there's a wall locating closely in front of the robot.

However, to be honest, the final system does not perform well. Here are the reasons and my suggestions if you plan to work on similar projects:
* Cheap stereo cameras (ELP Dual Lens Camera) are hard to calibrate and generate poor disparity maps. If you have enough budget, I would recommend using [Intel's RealSense camera](https://realsense.intel.com/) or depth camera. Their well-developed tools will not only save your time but give you better output.
* Cheap ultrasonic sensors (HC-SR04) perform poorly. They are good if you want to detect a wall with a distance less than 1m (although the standard range is 4m, it does not perform stablely when the distance is larger than 1m). However, the signals may bounce around in the room thus perform badly in a more complex environment, e.g. trying to detect a box. What's more, bear in mind that multiple ultrasonic sensors or multiple emissions may interfere with each other, too. If you insist on these distance-based sensors, I would suggest using the more promising [LiDAR sensor](https://irlock.com/products/tfmini-rangefinder?variant=15818579050547&utm_campaign=gs-2018-09-19&utm_source=google&utm_medium=smart_campaign&gclid=Cj0KCQiAtvPjBRDPARIsAJfZz0qQhvE5Wgyua1VzXPhsCDu_GOqgUyapprkPiMQiIYT7c_cRWPb5QysaAt5BEALw_wcB).

## Hardware List

## Software List