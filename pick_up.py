#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import _thread

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
    
# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=80, acceleration=120)
base_motor.control.limits(speed=80, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
touch_sensor = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
color_sensor = ColorSensor(Port.S2)

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(-30, 1000)
elbow_motor.run(40)
elbow_motor.run_time(35, 2000)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-60)
while not touch_sensor.pressed():
    wait(20)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)

COLORS = []

def color_identification(left, middle, middleright):
    global count
    POSSIBLE_COLORS = [Color.GREEN, Color.RED, Color.BLUE]
    
    color = color_sensor.color()
    
    if color == POSSIBLE_COLORS[0]:
        ev3.screen.print("Green")
        robot_release(left)
        count = 0
    elif color == POSSIBLE_COLORS[1]:
        ev3.screen.print("Red")
        robot_release(middle)
        count = 0
    elif color == POSSIBLE_COLORS[2]:
        ev3.screen.print("Blue")
        robot_release(middleright)
        count = 0
    else:
        count += 1


def robot_pick(position, pause=3000):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(100, position)
    # Lower the arm.
    elbow_motor.run_target(70, -38)
    wait(pause)

    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    gripper_motor.hold()

    if gripper_motor.angle() < -5:
        elbow_motor.run_target(70, 5)
        return True
    
    gripper_motor.run_target(200, -90)
    return False
    # Raise the arm to lift the wheel stack.

def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.

    # Rotate to the drop-off position.
    base_motor.run_target(200, position)
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(70, -40)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(70, 0)

#####
def set_location():
    """Returns the angles of the set position"""
    while Button.CENTER not in ev3.buttons.pressed():
        while Button.LEFT in ev3.buttons.pressed():
            base_motor.run(50)
        while Button.RIGHT in ev3.buttons.pressed():
            base_motor.run(-50)
        while Button.UP in ev3.buttons.pressed():
            elbow_motor.run(30)
        while Button.DOWN in ev3.buttons.pressed():
            elbow_motor.run(-30)

        base_motor.hold()
        elbow_motor.hold()

    elbow_angle = elbow_motor.angle()
    gripper_motor.run_target(200, -90)
    return (base_motor.angle(), elbow_angle)


def set_locations():
    """Set the pickup and drop off locations"""

    global PICKUP_LOCATION
    Locations = {}
    COLORS = {0: "NoColor", 1: "Red", 2: "Blue", 3: "Green"}

    MODE = 0
    if MODE == 0 or MODE == 1:
        ev3.screen.print("Set pickup location")

        PICKUP_LOCATION = set_location()
        wait(1000)
        ev3.screen.print("Position set")
        robot_pick(0)
        Locations["pickup"] = set_location()
        # set_more_locations = True
        MODE = 2
    
    if MODE == 2:
        ev3.screen.print("Set drop-off locations")
        ev3.screen.print("Click to set \nnew position")
        color = color_sensor.color()
        newDropOff = set_location()
        color_name = COLORS.get(color, "Unknown")
        Locations[color_name] = newDropOff
        ev3.screen.print(Locations)
        wait(1000)



    while set_more_locations:
        if Button.CENTER in ev3.buttons.pressed():
            if MODE == 0 or MODE == 1:
                if robot_pick(PICKUP_LOCATION): # Raden kan ej göra något ännu
                    color = color_identification()
                    color_name = color.get(color, 'unknown')
                    COLORS.append(color_name)
                    ev3.screen.print("Set new location")
                    ev3.screen.print("\n\nClick to set \nnew position")
                else:
                    set_more_locations = False
            # elif MODE == 2:
            #     if pickup(SHARED_LOCATION):
            #         color = read_color()
            #         COLORS.append(rgbp_to_hex(color))
            #         ev3.screen.print("Set new location")
            #         LOCATIONS.append(set_location())
            #         ev3.screen.print("Click to set \nnew position")
            #     else:
            #         set_more_locations = False

    # if MODE == 2:
    #     move_base(PICKUP_LOCATION)

#####

def mode_selection():
    """Lets the user select the robot mode"""
    ev3.screen.print("Left - start")  # ?
    global MODE
    MODE = -1
    while MODE == -1:
        if Button.LEFT in ev3.buttons.pressed():
            MODE = 0
            ev3.screen.print("Starting the program...")
    wait(1000)




paused = False  # Variable to track whether the robot is paused or not

def pause_program():
    global paused
    while True:
        if Button.UP in ev3.buttons.pressed():
            # Toggle the paused state when the UP button is pressed
            paused = not paused
            ev3.screen.print(paused)
            if paused == True:
                # If paused, stop all motors
                base_motor.stop()
                elbow_motor.stop()
                #gripper_motor.stop()
                ev3.screen.print("Paused")
                wait(5000)
            else:
                # If resumed, print a message and continue from where it was paused
                ev3.screen.clear()
                ev3.screen.print("Resumed")
        wait(100)

def stop_all():
    global stop_program
    while True:
        if Button.DOWN in ev3.buttons.pressed():
            ev3.screen.print("Emergency stop triggered!")
            ev3.speaker.beep()
            robot_release(50)
            stop_program = True
            break

# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
#
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.


stop_program = False

# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

# Define the three destinations for picking up and moving the wheel stacks.
LEFT = 200
MIDDLE = 100
MIDDLERIGHT = 150
RIGHT = 0

PICKUP_LOCATION = None
MODE = 0

# mode_selection()
set_locations()
_thread.start_new_thread(pause_program, ())
_thread.start_new_thread(stop_all, ())

count = 0
while (count < 4):
    if not stop_program:
    # Check if any button is pressed
    # Move a wheel stack from the right to the it's designated position.
        robot_pick(RIGHT)
        color_identification(LEFT, MIDDLE, MIDDLERIGHT)
        gripper_motor.run_target(200, -90)
    else:
        break
