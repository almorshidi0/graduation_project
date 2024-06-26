"""
PiCamera Module
=======================

This module provides a simple interface to capture images using the `picamera2` library on a Raspberry Pi.

Classes:
--------
- CameraController: A class to manage the initialization and capturing of images with the PiCamera.

Example Usage:
--------------
To use this module, create an instance of `CameraController` and call its methods.

    from picamera_module import CameraController

    camera_controller = CameraController()
    camera_controller.get_img('image.jpg')

To test this module, you can run it directly as a script. It will capture an image and save it as 'test_image.jpg'.

    $ python3 picamera_module.py

Dependencies:
-------------
- picamera2: Ensure that the `picamera2` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected camera module.
"""

from picamera2 import Picamera2
import cv2

class CameraController:
    """
    Class to control the PiCamera module.
    """
    def __init__(self):
        """
        Initialize the PiCamera module.
        """
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()

    def get_img(self, file_path='image'):
        """
        Capture an image and save it to the specified file path.

        Args:
            file_path: Path to save the captured image. Default is 'image.jpg'.
        """
        img_name = f"{file_path}.jpg"
        self.picam2.capture_file(img_name)
        img = cv2.imread(img_name)
        img = cv2.flip(img, -1)
        cv2.imwrite(img_name, img)
        print(f"Image captured and saved to {file_path}")

    def release(self):
        """Release the PiCamera resources."""
        self.picam2.stop()
        self.picam2.close()

def main():
    """
    Main function for module testing.

    This function creates an instance of `CameraController`, captures an image,
    and saves it as 'test_image.jpg' to test the camera control functions.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    print("Initializing the camera...")
    camera_controller = CameraController()
    print("Capturing image...")
    camera_controller.get_img('test_image0.jpg')
    camera_controller.release()
    print("Image captured and saved as 'test_image.jpg'.")

if __name__ == '__main__':
    main()
