"""
Data Collection Main Program
=========================

This script controls a car's movement using key presses and records data while the car is in motion.

It initializes modules for motor control, steering control, data collection, key press detection, and the PiCamera module for image capture.
The script continuously monitors key presses to adjust the car's speed and steering angle to control the car.
Key presses trigger various actions, such as adjusting speed and angle, starting and stopping recording, and terminating the program.
Recorded data includes images and corresponding speed and steering angle.

Modules:
--------
- data_collection_module    : Handles data collection and saving.
- key_press_module          : Manages key press detection and control.
- motor_module              : Control car movement.
- steering_module           : Control car steering.
- picamera_module           : Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- done      : Flag variable to terminate the program.
- record    : Flag variable to control recording status.
- key_val   : Current pressed key.
- key_old   : Last pressed key
- speed     : Speed
- angle     : Steering angle

Functions:
----------
- get_key_press()               : Get key press status and update global variables.
- update_movement_controls()    : Update speed and angle based on key presses.
- main()                        : Main function to control the car's movement, handle key presses, and manage data recording.


Key Presses:
------------
- RIGHT : Steer right.
- LEFT  : Steer left.
- UP    : Move forward.
- DOWN  : Move backward.
- r     : Start or stop recording.
- s     : Stop the car.
- k     : Terminate the program.

Example Usage:
--------------
To run the script, ensure the required modules (data_collection_module, key_press_module, motor_module, steering_module, picamera_module) are imported and available in the environment.

    $ python3 data_collection_main.py

Dependencies:
-------------
- data_collection_module    : Ensure that the `data_collection_module` module is properly implemented and available.
- key_press_module          : Ensure that the `key_press_module` module is properly implemented and available.
- motor_module              : Ensure that the `motor_module` module is properly implemented and available.
- steering_module           : Ensure that the `steering_module` module is properly implemented and available.
- picamera_module           : Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import os
from data_collection_module import DataCollector
from key_press_module       import KeyPressController
from motor_module           import MotorController
from steering_module        import SteeringController
from picamera_module        import CameraController

# Constants
KEY_LIST = ["RIGHT", "LEFT", "UP", "DOWN", "r", "s", "k"]
DEFAULT_SPEED = 1
DEFAULT_ANGLE = 0.7
ROI = (0.0, 0.2, 0.8, 0.8) # Ratio of interest

# Global Variables
done    = 0     # Flag variable to terminate the program
record  = 0     # Flag variable to control recording status
key_val = None  # Current pressed key
key_old = None  # Last pressed key
speed   = 0     # Initial speed
angle   = 0     # Initial steering angle
right_steering_error_handling = 0

# Initializing modules
data_collector = DataCollector()
data_collector.data_collection_init()

key_controller = KeyPressController()
key_controller.key_press_init()

motor_controller = MotorController(25, 23, 24)

steering_controller = SteeringController(18)

camera_controller = CameraController()

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
    if key_val == "RIGHT":
        angle = DEFAULT_ANGLE
    elif key_val == "LEFT":
        angle = -0.5
    elif key_val == "UP":
        speed = DEFAULT_SPEED
        angle = 0.1
    elif key_val == "DOWN":
        speed = -DEFAULT_SPEED
        angle = 0.1
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
    global speed, angle, record, done, key_val, key_old, right_steering_error_handling
    while True:
        angle = 0
        get_key_press()
        update_movement_controls()

        motor_controller.move(speed)
        if right_steering_error_handling == 1:
            if angle == 0:
                steering_controller.set_angle(DEFAULT_ANGLE)
                right_steering_error_handling = 0
        if angle < 0:
            right_steering_error_handling = 1
        steering_controller.set_angle(angle)
        
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
            data_collector.collect_data(camera_controller, new_path, speed, angle, roi=ROI)
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
            steering_controller.set_angle(0)
            steering_controller.detach()
            camera_controller.release()
            break

if __name__ == "__main__":
    main()
