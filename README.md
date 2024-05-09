# Sorting-robot

## Introduction

This README file provides a comprehensive overview of a robot made for sorting and transporting items based on colors, highlighting key functionalities such as a user interface to interact with the robot and a conveyor belt that transports items to a pickup location. This file also provides detailed instructions to get the code for the robot and how to set it up, and operating procedures to work with the robot.


## Getting started

-- Prerequisites
To get started with the Sorting Robot project using LEGO Mindstorms EV3 devices, you'll need:

* A computer with access to the internet and Bluetooth or a USB port for file transfer.
* LEGO Mindstorms EV3 software or another compatible third-party tool installed on your computer for deploying code to the EV3 device. We recommend using VSCode for this.
* A basic understanding of how to download files, navigate file systems, and transfer files to devices.

-- Installation and Setup
Here's a step-by-step guide to help you set up the Sorting Robot along with an optional Conveyor Belt:

    1. Download the Project:
        * Visit the project repository page on GitHub. It can be accessed via this link: 
        https://github.com/Hickek/Sorting-robot/tree/8d0c5d6faf5c607366564dfed4fd9b3e8fe268cb
        * Download the ZIP file containing the project code.
        * Unzip the file in a convenient location on your computer.
        * Download VSCode if you don't already have it
        * Download the EV3 mindstorms extension from VSCode

    2. Connect the Robot:
        * Transfer the sorter.py file to the EV3 device using the LEGO Mindstorms extension on VSCode
        * Repeat the process for the Conveyor Belt robot, transferring the 'conveyor.py' file to it.

    3. Set Up and Calibrate the Robots:
        * On the EV3 robot, navigate through the device interface to locate and run the sorter.py program
        * Follow any on-screen prompts to perform initial calibration and setup as necessary.

    4. Connect a conveyor belt:
        * If a conveyor belt is being used, please make sure the name of the sorting robot is ev3dev.
        If you want to use another name, you must change this line of code in the conveyor.py file:
        SERVER = 'ev3dev'
        * Upload the conveyor.py file to the conveyor belt.
        * Connect the sorting robot and conveyor belt via bluetooth.


## Building and running

Regular startup:
Download the program to the sorting robot and navigate the menu to the file sorter.py and select it.
In the menu that gets displayed after calibration, select 'No'.

Shutdown:
To shut down the robot, press the top left button on the robots interface.
This will immediately turn off all motors. It might result in the robot dropping any item it is currently holding so it is not recommended to do this if it is holding an object.

Emergency shutdow:
An emergency shutdown will slowly move the robot arm to the emergency zone and put down the object it is holding. This will not turn off the robot so a regular shutdown is required afterwards.
To do an emergency shutdown, you can either select 'Emergency Shutdown' in the menu or simply press the left button on the robots interface.
You will not be able to do this during the robots calibration phase, if you want to shut it down during the calibration you must do a regular shutdown.

Conveyor belt:
Follow these instructions;
1. Manually move the robot arm above the conveyor belt.
2. Start the sorting robot.
3. You will now see a menu where you have to choose to enable the belt or not, choose Yes.
4. Finally, turn on the conveyor.

Elevated positions:
To pick up from elevated positions you must move the robot arm above the elevated position before starting the robot.

Color sorting:
The robot can only handle items of 3 different colors at a time.
If you want to change the colors, turn off the robot and turn it back on again.

Pickup/Drop-off/Emergency zones:
The robot have the locations of the pickup, drop-off & emergency zones preprogrammed. These are set at the following angles:
Pickup = 180 degrees
Drop-off 1 = 0 degrees
Drop-off 2 = 45 degrees
Drop-off 3 = 90 degrees
Emergency = 135 degrees
You can change the angles for each zone in the menu when the robot is running. It is possible to change the locations to these values: 0, 45, 90, 135, 180 degrees.

Schedule/Timer:
The robot is preselected to never stop working but you have the option to manually select a duration for how long you want the robot to operate through the menu.
You have the following options: 1 min, 10 min, 30 min, 1 hour, nonstop running.


## Features

These are the requirements with completed requirements marked with an x and partially completed requirements marked as x* with a comment under

- [x] US01B: As a customer, I want the robot to pick up items from a designated position

- [x] US02B: As a customer, I want the robot to drop items off at a designated position

- [x*] US03: As a customer, I want the robot to be able to determine if an item is present at a given location.
* Comment: It can determine if an item is at the pickup location by trying to pick it up

- [x*] US04B: As a customer, I want the robot to tell me the color of an item at a designated position
* Comment: The robot will display the color of the item it last picked up if you click the up or down buttons in the main menu

- [x] US05: As a customer, I want the robot to drop items off at different locations based on the color of the item.

- [x] US06: As a customer, I want the robot to be able to pick up items from elevated positions.

- [x] US08 As a customer, I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones.

- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived.

- [x*] US10: As a customer, I want the robots to sort items at a specific time.
* Comment: It can not work through a schedule but can work on a timer with pre-selected values

- [] US11: As a customer, I want two robots (from two teams) to communicate and work together on items sorting without colliding with each other.

- [] US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons).

- [x*] US13: As a customer, I want to easily reprogram the pickup and drop off zone of the robot.
* Comment: You can only change the locations to 5 different values

- [x*] US14: As a customer, I want to easily change the schedule of the robot pick up task.
* Comment: It can not work through a schedule but can work on a timer with pre-selected values

- [x] US15: As a customer, I want to have an emergency stop button, that immediately terminates the operation of the robot safely.

- [x*] US16: As a customer, I want the robot to be able to pick an item up and put it in the designated drop-off location within 5 seconds.
* Comment: It takes approximately 6 seconds

- [x*] US17:As a customer, I want the robot to pick up items from a rolling belt and put them in the designated positions based on color and shape.
* Comment: It does not sort the items based on shape

- [x] US18: As a customer, I want to have a pause button that pauses the robot's operation when the button is pushed and then resumes the program from the same point when I push the button again.

- [x] Us19: As a customer, I want a very nice dashboard to configure the robot program and start some tasks on demand.
