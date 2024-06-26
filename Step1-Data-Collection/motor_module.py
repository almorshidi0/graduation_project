"""
PiCamera Module
=======================

This module provides a simple interface to control a Raspberry Pi camera using the `picamera` library.

Classes:
--------
- CameraController: A class to manage the initialization and control of the PiCamera.

Example Usage:
--------------
To use this module, create an instance of `CameraController` and call its methods.

    from picamera_module import CameraController

    camera_controller = CameraController()
    camera_controller.record_video('output.h264', duration=10)

To test this module, you can run it directly as a script. It will record a short video.

    $ python3 picamera_module.py

Dependencies:
-------------
- picamera: Ensure that the `picamera` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected PiCamera module.
"""

import picamera
from time import sleep

class CameraController:
    """
    Class to control a PiCamera module.
    """
    def __init__(self):
        """
        Initialize the PiCamera module.
        """
        self.camera = picamera.PiCamera()

    def record_video(self, filename, duration=10):
        """
        Record a video with the PiCamera for a specified duration.

        Args:
            filename: Name of the output video file.
            duration: Duration of the video recording in seconds. Default is 10 seconds.
        """
        self.camera.start_recording(filename)
        print(f"Recording video to '{filename}' for {duration} seconds...")
        sleep(duration)
        self.camera.stop_recording()
        print("Video recording stopped.")

    def capture_image(self, filename):
        """
        Capture a single image with the PiCamera.

        Args:
            filename: Name of the output image file.
        """
        self.camera.capture(filename)
        print(f"Captured image saved as '{filename}'.")

    def close(self):
        """Release the resources used by the PiCamera."""
        self.camera.close()

def main():
    """
    Main function for module testing.

    This function creates an instance of `CameraController`, initializes the camera, and
    performs a series of actions to test the camera control functions.

    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    """
    print("Initializing the PiCamera module...")
    camera_controller = CameraController()
    try:
        # Record a video
        print("Recording a test video...")
        camera_controller.record_video('output.h264', duration=10)
        sleep(2)

        # Capture an image
        print("Capturing a test image...")
        camera_controller.capture_image('test_image.jpg')
        sleep(2)
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
    finally:
        camera_controller.close()
        print("PiCamera module closed.")

if __name__ == '__main__':
    main()
