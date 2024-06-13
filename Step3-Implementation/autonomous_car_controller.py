"""
Autonomous Car Controller
=========================

This script controls an autonomous car's movement using a pre-trained model to predict speed and steering angle from camera input.

It initializes modules for controlling the DC motors and the PiCamera module for image capture.
The script continuously captures images, processes them, and uses a machine learning model to predict the speed and steering angle to control the car's movement.

Modules:
--------
- dc_motors_module: Controls the car's DC motors for movement.
- picamera_module: Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- motor: Instance of DcMotorController to control the motors.
- camera: Instance of PiCameraController to capture images.
- model: Pre-trained machine learning model for speed and angle prediction.

Functions:
----------
- preProcess(img): Preprocess the captured image for the model.
- main(): Main function to capture images, predict speed and angle, and control the car's movement.

Example Usage:
--------------
To run the script, ensure the required modules (dc_motors_module, picamera_module) are imported and available in the environment.

    $ python autonomous_car_controller.py

Dependencies:
-------------
- dc_motors_module: Ensure that the `dc_motors_module` module is properly implemented and available.
- picamera_module: Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from dc_motors_module import DcMotorController
from picamera_module import PiCameraController

# Initializing modules
motor = DcMotorController(17, 27, 22, 25, 23, 24)

camera_controller = PiCameraController()
roi = (0.0, 0.2, 0.8, 0.8) #ratio of interest
camera_controller.pi_cam_init(roi)

model_path = None
model = load_model(model_path)

def preProcess(img):
    """
    Preprocess the captured image for the model.

    Args:
        img (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: Preprocessed image.
    """
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # Convert to YUV color space
    img = cv2.GaussianBlur(img, (3, 3), 0)  # Apply Gaussian blur
    img = cv2.resize(img, (200, 66))  # Resize the image
    img = img / 255.0  # Normalize the image
    return img

def main():
    """
    Main function to capture images, predict speed and angle, and control the car's movement.

    This function continuously captures images, processes them, and uses a pre-trained model to predict the speed and steering angle to control the car's movement.
    """
    img_path = os.path.join(os.getcwd(), "road_img")
    while True:
        camera_controller.get_img(img_path)  # Capture image
        img = cv2.imread(img_path)
        img = np.asarray(img)  # Convert to numpy array
        img = preProcess(img)  # Preprocess the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        prediction = model.predict(img)  # Predict angle and speed
        angle = float(prediction[0][0])  # Extract angle
        speed = float(prediction[0][1])  # Extract speed

        print(f"Angle: {angle}, Speed: {speed}")  # Print values
        motor.move_forward(speed, angle)  # Control motors
        cv2.waitKey(1)  # Wait for 1 ms

if __name__ == "__main__":
    main()
