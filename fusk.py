stop_program = False
continue_main_loop = True
class RobotState:
    def init(self):
        self.gripper_position = None
        self.elbow_position = None
        self.base_position = None

Create an instance of RobotState to store the state
robot_state = RobotState()

Function to store robot state
def store_state():
    robot_state.gripper_position = gripper.angle()
    robot_state.elbow_position = elbow.angle()
    robot_state.base_position = base.angle()

Function to restore robot state
def restore_state():
    gripper.run_target(200, robot_state.gripper_position)
    elbow.run_target(200, robot_state.elbow_position)
    base.run_target(200, robot_state.base_position)

def emergency_check():
    global stop_program, button_ctrl
    while True:
            if not button_ctrl:
                if Button.UP in ev3.buttons.pressed():
                    ev3.speaker.beep()  # Optional: Makes a beep sound when the emergency stop is triggered
                    gripper.stop()
                    elbow.stop()
                    base.stop()
                    print("Emergency stop triggered!")
                    stop_program = True
                    break  # Exit the thread
                elif Button.LEFT in ev3.buttons.pressed():
                    pause()

def pause():
    global continue_main_loop, button_ctrl
    ev3.speaker.beep()
    gripper.hold()
    elbow.hold()
    base.hold()
    print("Paused!")
    continue_main_loop = False
    while not continue_main_loop:
        client.check_msg()
            if not button_ctrl:
                if Button.RIGHT in ev3.buttons.pressed():
                    resume()

Function to handle resuming
def resume():
    global continue_main_loop
    print("Resuming...")
    continue_main_loop = True
