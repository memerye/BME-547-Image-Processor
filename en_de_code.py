import base64
import numpy as np


def image_to_b64(img):
    """Encode the unit8 image to base64

    Args:
        img (ndarray): The image array, dtype=np.uint8

    Returns:
        string: The encoded string for the images
        tuple: The size of the image
    """
    size = img.shape
    b64_string = base64.b64encode(img.tobytes())
    return b64_string, size


def b64_to_image(base64_string, size):
    """Decode the base64 to uint8 image

    Args:
        base64_string (string): The encoded string for the images
        size (tuple): The size of the image

    Returns:
        ndarray: The decoded image
    """
    decode_img = np.frombuffer(base64.b64decode(base64_string), np.uint8)
    img = decode_img.reshape(size)
    return img


if __name__ == '__main__':
    img = np.uint8(np.array([[1, 2, 3], [4, 5, 6]]))
    img_b64_string, size = image_to_b64(img)
    decode_img = b64_to_image(img_b64_string, size)
    assert decode_img.tolist() == img.tolist()
    print("success!")
