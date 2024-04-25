paused = False  # Variable to track whether the robot is paused or not

def stop_program():
    global paused
    while True:
        if Button.UP in ev3.buttons.pressed():
            # Toggle the paused state when the UP button is pressed
            paused = not paused
            if paused:
                # If paused, stop all motors
                base_motor.stop()
                elbow_motor.stop()
                gripper_motor.stop()
                ev3.screen.print("Paused")
            else:
                # If resumed, print a message and continue from where it was paused
                ev3.screen.clear()
                ev3.screen.print("Resumed")
        wait(100)

# Start the stop_program function
stop_program()

# Main loop
count = 0
while count < 4:
    if not paused:
        # Continue with your robot operation if it's not paused
        robot_pick(RIGHT)
        color_identification()
        gripper_motor.run_target(200, -90)
        count += 1
