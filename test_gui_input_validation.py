# test_gui_input_validation.py
import pytest


@pytest.mark.parametrize('filename, expected', [
    (['test.png', 'test.jpg', 'test.tif', 'test.zip'], 'zip and multiple'),
    (['test.zip', 'test.tif', 'test2.zip'], 'zip and multiple'),
    (['test.png', 'test.jpg', 'test.tif'], 'multiple img'),
    (['test.png'], 'img'),
    (['test.zip'], 'zip'),
])
def test_ck_type(filename, expected):
    """Test the function ck_type that checks combination of selected file types
    and categorizes them

    Args:
        filename: a list of file names as strings
        expected: expected output categorization

    Returns:
        Boolean
    """
    from gui import ck_type
    file_type = ck_type(filename)
    assert file_type == expected
