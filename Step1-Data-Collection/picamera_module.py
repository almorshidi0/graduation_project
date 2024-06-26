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

from picamera import PiCamera

class PiCameraController:
    def __init__(self):
        self.pi_cam = None

    def pi_cam_init(self, roi=None):
        self.pi_cam = PiCamera()

        # Adjust camera settings
        self.pi_cam.resolution = (2592, 1944)  # Adjust resolution as needed
        self.pi_cam.hflip = True
        self.pi_cam.vflip = True

        # Optionally set the region of interest (ROI)
        if roi:
            self.pi_cam.zoom = roi

    def get_img(self, file_name):
        self.pi_cam.capture(f"{file_name}.jpg")

    def close(self):
        if self.pi_cam:
            self.pi_cam.close()  # Close the camera instance

def main():
    camera_controller = PiCameraController()
    try:
        camera_controller.pi_cam_init()
        camera_controller.get_img("test_1")
        roi0 = (0.0, 0.2, 0.8, 0.8)
        camera_controller.pi_cam_init(roi=roi0)
        camera_controller.get_img("test_0")
    finally:
        camera_controller.close()

if __name__ == '__main__':
    main()
