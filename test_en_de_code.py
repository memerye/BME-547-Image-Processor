# test_en_de_code.py
import pytest
import numpy as np


@pytest.mark.parametrize("img", [
    (np.uint8(np.array([1, 2, 3]))),
    (np.uint8(np.array([[1, 2, 3], [3, 4, 5]])))
])
def test_en_de_code(img):
    """Test the functions image_to_b64 and b64_to_image
    that encode and decode the image

    Args:
        img (ndarray): The image array, dtype=np.uint8

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from en_de_code import image_to_b64, b64_to_image
    img_b64_string, size = image_to_b64(img)
    decode_img = b64_to_image(img_b64_string, size)
    assert decode_img.tolist() == img.tolist()
