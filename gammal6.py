def stop_all():
    global stop_program
    while True:
        if Button.DOWN in ev3.buttons.pressed():
            ev3.speaker.beep()
            elbow_motor.run_target(60, -40)
            gripper_motor.run_target(200, -90)
            elbow_motor.run_target(60, 0)
            for motor in (gripper_motor, elbow_motor, base_motor):
                motor.stop()
            ev3.screen.print("Emergency stop triggered!")
            stop_program = True
            break 
