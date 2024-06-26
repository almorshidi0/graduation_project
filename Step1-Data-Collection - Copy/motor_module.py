"""
DC Motors Module
=======================

This module provides a simple interface to control a small car prototype with four DC motors using the `Rpi.GPIO` library.

Classes:
--------
- MotorController: A class to manage the initialization and control of the DC motors.

Example Usage:
--------------
To use this module, create an instance of `MotorController` and call its methods.

    from motor_module import MotorController

    motor_controller = MotorController(ena1, in1, in2)
    motor_controller.move(0.6)

To test this module, you can run it directly as a script. It will perform a series of movements.

    $ python3 motor_module.py

Dependencies:
-------------
- Rpi.GPIO: Ensure that the `Rpi.GPIO` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with connected DC motors.
"""

import RPi.GPIO as GPIO
from time import sleep

class MotorController:
    """
    Class to control a DC motor module consisting of two motors.
    """
    def __init__(self, ena1, in1, in2):
        """
        Initialize the DC motor module with the specified GPIO pins.

        Args:
            ena1: GPIO pin for motor enable 1 (ENA1).
            in1: GPIO pin for motor input 1 (IN1).
            in2: GPIO pin for motor input 2 (IN2).
        """
        self.ena1 = ena1
        self.in1 = in1
        self.in2 = in2
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ena1, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.ena1, 100)  # PWM at 100Hz
        self.pwm.start(0)

    def move(self, speed=0.5):
        """
        Move the motor forward with the specified speed.

        Args:
            speed: Speed of motion, ranging from -1 (full backward) to 1 (full forward). Default is 0.5.
        """
        speed = max(-1, min(1, speed))
        duty_cycle = abs(speed) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if speed < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        else:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)

    def stop(self):
        """Stop the motor."""
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def release(self):
        """Release the GPIO resources used by the motor."""
        self.pwm.stop()
        GPIO.cleanup()

def main():
    """
    Main function for module testing.

    This function creates an instance of `MotorController`, initializes the motors, and
    performs a series of movements to test the motor control functions.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    print("Let's introduce our motors to our PI!")
    motor_controller = MotorController(25, 23, 24)
    print("Let's go!")
    try:
        while True:
            # Move Forward
            motor_controller.move(1)
            sleep(2)
            print("The car is moving forward!")
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
            
            # Move Backward
            motor_controller.move(-1)
            print("The car is moving backward!")
            sleep(2)
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
    except KeyboardInterrupt:
        motor_controller.stop()
        motor_controller.release()
        print()
        print("The car is now dead!")

if __name__ == '__main__':
    main()
