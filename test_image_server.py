# test_image_server.py
import pytest
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
