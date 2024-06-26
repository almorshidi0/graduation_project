"""
Pi Camera Module
=======================

This module provides a simple interface to control a Pi Camera for capturing images and videos on a Raspberry Pi.

Classes:
--------
- CameraController: A class to manage the initialization and control of the Pi Camera.

Example Usage:
--------------
To use this module, create an instance of `CameraController` and call its methods.

    from picamera_module import CameraController

    camera_controller = CameraController()
    camera_controller.capture_image('image.jpg')

To test this module, you can run it directly as a script. It will capture an image and save it to the current directory.

    $ python3 picamera_module.py

Dependencies:
-------------
- picamera: Ensure that the `picamera` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected Pi Camera.
"""

from picamera import PiCamera
from time import sleep

class CameraController:
    """
    Class to control a Pi Camera module.
    """
    def __init__(self):
        """
        Initialize the Pi Camera module.
        """
        self.camera = PiCamera()

    def capture_image(self, filename):
        """
        Capture an image with the Pi Camera and save it to a file.

        Args:
            filename: Name of the file to save the captured image.
        """
        self.camera.capture(filename)
        print(f"Captured image saved as {filename}")

    def close(self):
        """Release the Pi Camera resources."""
        self.camera.close()

def main():
    """
    Main function for module testing.

    This function creates an instance of `CameraController`, initializes the camera,
    captures an image, records a video, and releases resources.

    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.

    Args:
    None

    Returns:
    None
    """
    print("Initializing Pi Camera...")
    camera_controller = CameraController()
    
    try:
        # Capture an image
        print("Capturing an image...")
        camera_controller.capture_image('image.jpg')
        sleep(2)
        
    finally:
        # Cleanup
        camera_controller.close()
        print("Pi Camera module closed.")

if __name__ == '__main__':
    main()
