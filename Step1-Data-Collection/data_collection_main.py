"""
Data Collection Main Program
=========================

This script controls a car's movement using key presses and records data while the car is in motion.

It initializes modules for data collection, key press detection, control of DC motors, and the PiCamera module for image capture.
The script continuously monitors key presses to adjust the car's speed and steering angle .
Key presses trigger various actions, such as adjusting speed and angle, starting and stopping recording, and terminating the program.
Recorded data includes images and corresponding speed and steering angle.

Modules:
--------
- data_collection_module: Handles data collection and saving.
- key_press_module: Manages key press detection and control.
- dc_motors_module: Controls the car's DC motors for movement.
- picamera_module: Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- done      : Flag variable to terminate the program.
- record    : Flag variable to control recording status.
- key_val   : Current pressed key.
- key_old   : None Last pressed key
- speed     : Speed
- angle     : Steering angle

Functions:
----------
- main(): Main function to control the car's movement, handle key presses, and manage data recording.

Key Presses:
------------
- RIGHT: Increase speed and steer right.
- LEFT: Increase speed and steer left.
- UP: Increase speed.
- DOWN: Decrease speed.
- r: Start or stop recording.
- s: Stop the car.
- k: Terminate the program.

Example Usage:
--------------
To run the script, ensure the required modules (data_collection_module, key_press_module, dc_motors_module, picamera_module) are imported and available in the environment.

    $ python3 data_collection_main.py

Dependencies:
-------------
- data_collection_module: Ensure that the `data_collection_module` module is properly implemented and available.
- key_press_module: Ensure that the `key_press_module` module is properly implemented and available.
- dc_motors_module: Ensure that the `dc_motors_module` module is properly implemented and available.
- picamera_module: Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""


# Importing necessary modules
import os
from data_collection_module import DataCollector
from key_press_module       import KeyPressController
from dc_motors_module       import DcMotorController
from picamera_module        import PiCameraController

# Constants
KEY_LIST = ["RIGHT", "LEFT", "UP", "DOWN", "r", "s", "k"]

# Global Variables
done    = 0     # Flag variable to terminate the program
record  = 0     # Flag variable to control recording status
key_val = None  # Current pressed key
key_old = None  # Last pressed key
speed   = 0     # Initial speed
angle   = 0     # Initial steering angle

# Initializing modules
data_collector = DataCollector()
data_collector.data_collection_init()

key_controller = KeyPressController()
key_controller.key_press_init()

motor_controller = DcMotorController(17, 27, 22, 25, 23, 24)

camera_controller = PiCameraController()
roi = (0.0, 0.2, 0.8, 0.8) #ratio of interest
camera_controller.pi_cam_init(roi)

def get_key_press():
    """
    Get key press status and update global variables.
    
    This function checks the status of each key in the KEY_LIST and updates the key_val accordingly.
    
    Args:
        None
    
    Returns:
        None
    """
    global key_val
    for key in KEY_LIST:
        if key_controller.get_key_status(key):
            key_val = key
            break

def update_movement_controls():
    """
    Update speed and angle based on key presses.
    
    This function updates the speed and angle variables based on the current pressed key.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done, key_val, key_old
    print(key_val)
    if key_val == "RIGHT":
        speed = 0.6
        angle = speed
    elif key_val == "LEFT":
        speed = 0.6
        angle = -speed
    elif key_val == "UP":
        speed = 0.4
        angle = 0
    elif key_val == "DOWN":
        speed = -0.4
        angle = 0
    elif key_val == "s":
        speed = 0
        angle = 0
    elif key_val == "k":
        done += 1
    elif key_val == key_old:
        pass
    elif key_val == "r":
        key_old = key_val
        record += 1
    if key_val != "r":
        key_val = None
        key_old = None

def main():
    """
    Main function to control the car's movement.
    
    This function continuously monitors key presses, updates movement controls, and manages data recording.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done, key_val, key_old
    while True:
        speed = 0.4
        angle = 0
        get_key_press()
        update_movement_controls()

        # Control vehicle movement
        if speed > 0:
            motor_controller.move_forward(speed, angle)
            speed = 0.4
        elif speed < 0:
            motor_controller.move_backward(-speed, angle)
        else:
            motor_controller.stop()

        # Start recording
        if record == 1:
            print("Recording Started ...")
            while os.path.exists(os.path.join(data_collector.data_directory, f"img{str(data_collector.folder_index)}")):
                data_collector.folder_index += 1
            new_path = os.path.join(data_collector.data_directory, f"img{str(data_collector.folder_index)}")
            os.makedirs(new_path)
            record += 1
        # Collect data
        if record == 2:
            data_collector.collect_data(camera_controller, new_path, speed, angle)
        # Save data and reset
        elif record == 3:
            record = 0
            data_collector.save_log()
            data_collector.img_list.clear()
            data_collector.speed_list.clear()
            data_collector.angle_list.clear()

        # Terminate program
        if done != 0:
            motor_controller.stop()
            motor_controller.release()
            break

if __name__ == "__main__":
    main()
