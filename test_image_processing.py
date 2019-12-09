# test_image_processing.py
import pytest
import numpy as np


@pytest.mark.parametrize("img, expected", [
    (np.uint8(np.array([1, 2, 3])), np.uint8(np.array([1, 2, 3]))),
    (np.float64(np.array([0.2, 0.3, 0.8])), np.uint8(np.array([51, 76, 204]))),
    (np.float64(np.array([1, 2, 3])), np.uint8(np.array([1, 2, 3]))),
    (np.uint16(np.array([1, 2, 3])), np.uint8(np.array([1, 2, 3])))
])
def test_convert_image_to_uint8(img, expected):
    """Test the functions convert_image_to_uint8
    that can convert the float64 images to uint8

    Args:
        img (ndarray): The image array
        expected (ndarray): The expected image array with uint8 data

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_processing import convert_image_to_uint8
    uint8_image = convert_image_to_uint8(img)
    assert uint8_image.tolist() == expected.tolist()


@pytest.mark.parametrize("img, expected", [
    (np.uint8(np.array([1, 2, 3])), np.uint8(np.array([0, 127, 255]))),
    (np.uint8(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
     np.uint8(np.array([[0, 31, 63], [95, 127, 159], [191, 223, 255]])))
])
def test_constr(img, expected):
    """Test the functions constr in ImageProcessing class
    that can achieve contrast stretching.

    Args:
        img (ndarray): The image array
        expected (ndarray): The expected image array after contrast stretching.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_processing import ImageProcessing
    I = ImageProcessing(img)
    processed_img, _ = I.constr()
    assert processed_img.tolist() == expected.tolist()


@pytest.mark.parametrize("img, expected", [
    (np.uint8(np.array([1, 2, 3])), np.uint8(np.array([254, 253, 252]))),
    (np.uint8(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
     np.uint8(np.array([[254, 253, 252], [251, 250, 249], [248, 247, 246]])))
])
def test_constr(img, expected):
    """Test the functions invert in ImageProcessing class
    that can achieve inverting color.

    Args:
        img (ndarray): The image array
        expected (ndarray): The expected image array after inverting color.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_processing import ImageProcessing
    I = ImageProcessing(img)
    processed_img, _ = I.invert()
    assert processed_img.tolist() == expected.tolist()
