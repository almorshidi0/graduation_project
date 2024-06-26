from picamera2 import Picamera2

pi_camera = Picamera2()
pi_camera.start()

def get_img(file_name):
    """
    Capture an image and save it with the provided file name.

    Args:
    file_name (str): The name to save the image file as.

    Returns:
    None
    """
    pi_camera.capture_file(f"{file_name}.jpg")

if __name__ == '__main__':
    count = 0 
    while True:
        get_img(f"test_{count}")
        count += 1