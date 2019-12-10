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


@pytest.mark.parametrize('index, expected', [
    (0, 'Histogram Equalization'),
    (1, 'Contrast Stretching'),
    (2, 'Log Compression'),
    (3, 'Invert Image'),
    (4, False)
])
def test_cvt_proc_index(index, expected):
    """Test the function cvt_proc_index that converts process index
    into process name

    Args:
        index: a process index
        expected: expected output process name

    Returns:
        Boolean
    """
    from gui import cvt_proc_index
    name = cvt_proc_index(index)
    assert name == expected
