"""
Steering Servo Module
======================

This module provides a simple interface to control a steering servo motor using the `gpiozero` library.

Classes:
--------
- SteeringController: A class to manage the initialization and control of the steering servo motor.

Example Usage:
--------------
To use this module, create an instance of `SteeringController` and call its methods.

    from steering_module import SteeringController

    steering_controller = SteeringController()
    steering_controller.set_angle(0.75)

To test this module, you can run it directly as a script. It will perform a series of movements.

    $ python3 steering_module.py

Dependencies:
-------------
- gpiozero: Ensure that the `gpiozero` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected servo motor.
"""

from gpiozero import Servo
from time import sleep

class SteeringController:
    """
    Class to control a steering servo motor.
    """
    def __init__(self, pin=17):
        """
        Initialize the servo motor with the specified GPIO pin.

        Args:
            pin: GPIO pin for the servo signal. Default is 17.
        """
        self.servo = Servo(pin)

    def set_angle(self, ratio):
        """
        Set the servo angle based on a ratio.

        Args:
            ratio: Ratio for the angle, ranging from -1 (minimum position) to 1 (maximum position).
        """
        ratio = max(-1, min(1, ratio))
        self.servo.value = ratio

    def detach(self):
        """Release the GPIO resources used by the servo."""
        self.servo.detach()

def main():
    """
    Main function for module testing.

    This function creates an instance of `SteeringController`, initializes the servo, and
    performs a series of movements to test the servo control functions.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    print("Let's introduce our steering servo motor to our PI!")
    steering_controller = SteeringController(18)
    right_steering_error_handling = 0
    print("Let's go!")
    try:
        while True:
            # Set angle to maximum (1.0)
            print("Setting angle to maximum (0.5)")
            steering_controller.set_angle(0.5)
            sleep(2)

            # Set angle to middle (0.0)
            print("Setting angle to middle (0.0)")
            steering_controller.set_angle(0.0)
            sleep(2)

            # Set angle to minimum (-1.0)
            print("Setting angle to minimum (-0.5)")
            steering_controller.set_angle(-0.5)
            right_steering_error_handling = 1
            sleep(2)
            
            # Set angle to middle (0.0)
            print("Setting angle to middle (0.0)")
            if right_steering_error_handling == 1:
                steering_controller.set_angle(0.5)
                right_steering_error_handling = 0
            steering_controller.set_angle(0.0)
            sleep(2)

            # Sweep back and forth
            print("Sweeping back and forth")
            for ratio in [-0.5, 0, 0.5, 0]:
                if right_steering_error_handling == 1:
                    if ratio == 0:
                        steering_controller.set_angle(0.5)
                        right_steering_error_handling = 0
                if ratio < 0:
                    right_steering_error_handling = 1
                steering_controller.set_angle(ratio)
                sleep(2)
            
    except KeyboardInterrupt:
        steering_controller.detach()
        print()
        print("Steering servo motor control terminated!")

if __name__ == '__main__':
    main()
