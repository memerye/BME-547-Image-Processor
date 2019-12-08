# test_image_server.py
import pytest
import numpy as np
from pymodm import connect


@pytest.mark.parametrize("user_info, expected", [
    ({"user_id": "1"}, True),
    ({"user1d": "1"}, False)
])
def test_validate_user_keys(user_info, expected):
    """Test the function validate_user_keys.

    Args:
        user_info (dict): the posted user data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_user_keys
    result = validate_user_keys(user_info)
    assert result == expected


@pytest.mark.parametrize("user_info, expected", [
    ({"user_id": "123"}, "123"),
    ({"user_id": "Aaa"}, "Aaa"),
    ({"user_id": "a1"}, "a1"),
    ({"user_id": "    a 1"}, "a1"),
    ({"user_id": "a_1"}, "a_1"),
    ({"user_id": "1+"}, False),
    ({"user_id": 1}, False)
])
def test_validate_id(user_info, expected):
    """Test the function validate_id.

    Args:
        user_info (dict): the posted user data.
        expected (bool or int): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_id
    result = validate_id(user_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"userid": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "Image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "image_name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "img_size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False)
])
def test_validate_image_keys(image_info, expected):
    """Test the function validate_image_keys.

    Args:
        image_info (dict): the posted image data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_image_keys
    result = validate_image_keys(image_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"user_id": "123",
      "image": "pseudo_encoeded1",
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": [np.array([1, 2, 3]), np.array([4, 5, 6]), "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False)
])
def test_validate_images(image_info, expected):
    """Test the function validate_images.

    Args:
        image_info (dict): the posted image data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_images
    result = validate_images(image_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": "01.jpg",
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": [1, 2, 3],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01jpg", "02jpg", "03jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False)
])
def test_validate_image_names(image_info, expected):
    """Test the function validate_image_names.

    Args:
        image_info (dict): the posted image data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_image_names
    result = validate_image_names(image_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": (200, 300, 3)}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], (100, 150, 3), [180, 180, 1]]}, False),
])
def test_validate_size(image_info, expected):
    """Test the function validate_size.

    Args:
        image_info (dict): the posted image data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_size
    result = validate_size(image_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encoeded1", "pseudo_encoeded2", "pseudo_encoeded3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3]]}, False)
])
def test_validate_data_length(image_info, expected):
    """Test the function validate_data_length.

    Args:
        image_info (dict): the posted image data.
        expected (bool): the expected result of the function.

    Returns:
        Error if the test fails
        Pass if the test passes
    """
    from image_server import validate_data_length
    result = validate_data_length(image_info)
    assert result == expected
