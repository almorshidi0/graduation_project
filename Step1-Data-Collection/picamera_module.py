"""
PiCamera Module
===============

This module provides a simple interface to initialize the PiCamera and capture images using the `picamera2` library.

Classes:
--------
- PiCameraController: A class to manage the PiCamera initialization and image capture.

Example Usage:
--------------
To use this module, create an instance of `PiCameraController` and call its methods.

    from picamera_module import PiCameraController

    camera_controller = PiCameraController()
    camera_controller.pi_cam_init()
    camera_controller.get_img("example_image")

To test this module, you can run it directly as a script. It will initialize the camera and capture 10 images named 'test_0.jpg' to 'test_9.jpg'.

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
import time

class PiCameraController:
    def __init__(self):
        """
        Initialize the PiCameraController class.
        """
        self.pi_cam = None

    def pi_cam_init(self, roi=None):
        """
        Initialize and start the PiCamera with error handling.

        Args:
        roi (tuple, optional): A tuple defining the region of interest (ROI) as (x, y, width, height).
                            Each value should be a proportion of the total image dimensions (0.0 to 1.0).
        
        Returns:
        None
        """
        try:
            self.pi_cam = Picamera2()
            config = self.pi_cam.create_still_configuration()
            self.pi_cam.configure(config)
            self.pi_cam.start()

            # Allow the camera to warm up
            time.sleep(2)

            if roi:
                self.pi_cam.set_controls({"ScalerCrop": roi})
        except Exception as e:
            print(f"Error initializing camera: {e}")
            # Optionally, handle the error or raise it further

    def get_img(self, file_name):
        """
        Capture an image and save it with the provided file name.

        Args:
        file_name (str): The name to save the image file as, without file extension.
        
        Returns:
        None
        """
        img_name = f"{file_name}.jpg"
        self.pi_cam.capture_file(img_name)
        img = cv2.imread(img_name)
        img = cv2.flip(img, -1)  # Flip horizontally and vertically
        cv2.imwrite(img_name, img)

def main():
    """
    Main function for module testing.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    camera_controller = PiCameraController()
    camera_controller.pi_cam_init()
    camera_controller.get_img("test_1")
    roi0 = (0.0, 0.2, 0.8, 0.8)
    camera_controller.pi_cam_init(roi=roi0)
    camera_controller.get_img("test_0")

if __name__ == '__main__':
    main()
