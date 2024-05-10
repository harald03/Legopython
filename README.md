# PA1473 - Software Development: Agile Project

## Introduction


This project involves the development of a Python script for controlling a lego robotic arm utilizing the EV3 Brick platform. The objective is to program the robotic arm to perform tasks including object manipulation and color sorting.

## Getting started

**Prerequisites:**
- A Lego robot with EV3 Brick.
- A computer.

**Setup Instructions:**
1. Clone the project repository to your local computer.
2. Connect your computer to the EV3 Brick using a USB cable.
3. Transfer the `main.py` script to your EV3 Brick using vs code or any other code editor that supports EV3 development.

## Building and running

**Running the Program:**
1. Power on the EV3 Brick.
2. Select the `main.py` file that was upploaded to the EV3 Brick.
3. Follow the instructions on the EV3 Brick.
4. In order to use the emergency stop button press the button down.

**Arguments and Controls:**
- When the pick-up and drop-off locations have been set the robot will continue sorting the objects util the stop button is pressed or the robot doesnt have any objectd to pick up in four attempts.
- In the set-up stage the robot will start by saving the pick-up location that is manually set by the user.
- When the drop-off is being set the robot will first pick-up an object and observe its color before the user can set the location for the designated color.

## Features

**Implemented User Stories:**
- [x] **US01:** As a customer, I want the robot to pick up items from a designated position.
- [x] **US02:** As a customer, I want the robot to drop items off at a designated position.
- [x] **US03:** As a customer, I want the robot to be able to determine if an item is present at a given location.
- [x] **US04:** As a customer, I want the robot to tell me the color and shape of an item at a designated position.
- [x] **US05:** As a customer, I want the robot to drop items off at different locations based on the color of the item.
- [x] **US06:** As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] **US07/08:** As a customer, I want to be able to calibrate a maximum of three different colors and assign them to specific drop-off zones.
- [x] **US09:** As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived.
- [x] **US10:** As a customer, I want the robots to sort items at a specific time.
- [ ] **US11:** As a customer, I want two robots (from two teams) to communicate and work together on items sorting without colliding with each other.
- [X] **US12:** As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons).
- [ ] **US13:** As a customer, I want to easily reprogram the pickup and drop off zone of the robot.
- [ ] **US14:** As a customer, I want to easily change the schedule of the robot pick up task.
- [x] **US15:** As a customer, I want to have an emergency stop button, that immediately terminates the operation of the robot safely.
- [x] **US16:** As a customer, I want the robot to be able to pick an item up and put it in the designated drop-off location within 5 seconds.
- [ ] **US17:** As a customer, I want the robot to pick up items from a rolling belt and put them in the designated positions based on color and shape.
- [ ] **US18:** As a customer, I want to have a pause button that pauses the robot's operation when the button is pushed and then resumes the program from the same point when I push the button again.
- [ ] **US19:** As a customer, I want a very nice dashboard to configure the robot program and start some tasks on demand.
