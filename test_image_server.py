# test_image_server.py
import pytest
import numpy as np
from image_processing import ImageProcessing

global I
I = ImageProcessing(np.uint8(np.array([1, 2, 3])))


@pytest.mark.parametrize("user_info, expected", [
    ({"user_id": "1"}, True),
    ({"user1d": "1"}, False)
])
def test_validate_user_keys(user_info, expected):
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
    from image_server import validate_id
    result = validate_id(user_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123",
      "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, True),
    ({"userid": "123",
      "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False),
    ({"user_id": "123",
      "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]]}, False)
])
def test_validate_image_keys(image_info, expected):
    from image_server import validate_image_keys
    result = validate_image_keys(image_info)
    assert result == expected


@pytest.mark.parametrize("images, expected", [
    (["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"], True),
    ("pseudo_encode1", False),
    ([np.array([1, 2, 3]), np.array([4, 5, 6]), "pseudo_encode3"], False)
])
def test_validate_images(images, expected):
    from image_server import validate_images
    result = validate_images(images)
    assert result == expected


@pytest.mark.parametrize("names, expected", [
    (["01.jpg", "02.jpg", "03.jpg"], True),
    ("01.jpg", False),
    ([1, 2, 3], False),
    (["01jpg", "02jpg", "03jpg"], False)
])
def test_validate_image_names(names, expected):
    from image_server import validate_image_names
    result = validate_image_names(names)
    assert result == expected


@pytest.mark.parametrize("size, expected", [
    ([[200, 300, 3], [100, 150, 3], [180, 180, 1]], True),
    ((200, 300, 3), False),
    ([200, 300, 3], False),
    ([[200], [300], [3]], False),
    ([[20.5, 300, 3], [10.3, 150, 3], [180, 180, 1]], False)
])
def test_validate_size(size, expected):
    from image_server import validate_size
    result = validate_size(size)
    assert result == expected


@pytest.mark.parametrize("image, name, size, expected", [
    (["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
     ["01.jpg", "02.jpg", "03.jpg"],
     [[200, 300, 3], [100, 150, 3], [180, 180, 1]], True),
    (["pseudo_encode1", "pseudo_encode2"],
     ["01.jpg", "02.jpg", "03.jpg"],
     [[200, 300, 3], [100, 150, 3], [180, 180, 1]], False),
    (["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
     ["01.jpg", "02.jpg"],
     [[200, 300, 3], [100, 150, 3], [180, 180, 1]], False),
    (["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
     ["01.jpg", "02.jpg", "03.jpg"],
     [[200, 300, 3], [100, 150, 3]], False)
])
def test_validate_data_length(image, name, size, expected):
    from image_server import validate_data_length
    result = validate_data_length(image, name, size)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123", "operation": 0,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, True),
    ({"userid": "123", "operation": 0,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, False),
    ({"user_id": "123", "operation": 0,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, False)
])
def test_validate_process_keys(image_info, expected):
    from image_server import validate_process_keys
    result = validate_process_keys(image_info)
    assert result == expected


@pytest.mark.parametrize("image_info, expected", [
    ({"user_id": "123", "operation": 0,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, 0),
    ({"user_id": "123", "operation": "histeq",
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, False),
    ({"user_id": "123", "operation": 0.3,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, False),
    ({"user_id": "123", "operation": 10,
      "raw_img": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
      "size": [[200, 300, 3], [100, 150, 3], [180, 180, 1]],
      "name": ["01.jpg", "02.jpg", "03.jpg"]}, False)
])
def test_validate_operation(image_info, expected):
    from image_server import validate_operation
    result = validate_operation(image_info)
    assert result == expected


@pytest.mark.parametrize("img, operation, expected", [
    (np.array([1, 2, 3]), 0, I.histeq()[0]),
    (np.array([1, 2, 3]), 1, I.constr()[0]),
    (np.array([1, 2, 3]), 2, I.logcom()[0]),
    (np.array([1, 2, 3]), 3, I.invert()[0])
])
def test_process_image(img, operation, expected):
    from image_server import process_image
    p_img, _ = process_image(img, operation)
    assert p_img.tolist() == expected.tolist()
