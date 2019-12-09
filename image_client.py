# image_client.py
import requests
from skimage import io
from en_de_code import image_to_b64, b64_to_image
import os


def post_user_id(info):
    """The client function of posting a new user.

    Args:
        info (dict): the dictionary of user's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/new_user",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)
    return None


def test_add_patients():
    """Create pseudo-lists of user information to add into the
    server and database.

    The pseudo-lists of users contain errors of:
    (1) Wrong dictionary key
    (2) Wrong format of id
    Ultimately three valid patient information will be added into
    the database with the id of "1_a", "08563", "Lily121".

    Returns:
        None
    """
    u_info = [{"userid": "1"},
              {"user_id": "1+a"},
              {"user_id": "1_a"},
              {"user_id": "08563"},
              {"user_id": "  Lily121"}]
    for info in u_info:
        post_user_id(info)
    return None


def request_check_id():
    """The client function of checking the existence of this id.

    The pseudo-lists of ids are expected as:
    * "whoisthis" doesn't exist in tha database
    * "1_a", "08563", and "Lily121" have already registered into the database
    The results will be printed out.

    Returns:
        None
    """
    ids = ["1_a", "08563", "Lily121", "whoisthis"]
    for p_id in ids:
        r = requests.get("http://127.0.0.1:5000/api/check_id/{}".format(p_id))
        print(r)
        print(r.status_code)
        if r.status_code == 200:
            answer = r.json()
            print(answer)
    return None


def post_images(info):
    """The client function of posting images.

    Args:
        info (dict): The dictionary of image information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/upload_images",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)
    return None


def test_add_images():
    """Create pseudo-lists of user information to
    add into the server and database.

    The pseudo-lists of image information contain errors of:
    (1) Wrong dictionary key
    (2) Wrong format of image
    (3) Wrong format of image name
    (4) Wrong format of image size
    (5) The lengths of images, their names and their size are not equal
    (6) Not existed id
    Ultimately three valid image information will be added into
    the database with the id of "1_a".

    Returns:
        None
    """
    u_info = [{"userid": "1_a",
               "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
               "name": ["01.jpg", "02.jpg", "03.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1_a",
               "image": "pseudo_encode1",
               "name": ["01.jpg", "02.jpg", "03.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1_a",
               "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
               "name": ["01jpg", 2, "03.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1_a",
               "image": ["pseudo_encode1"],
               "name": ["01.jpg"],
               "size": (10, 10, 3)},
              {"user_id": "1_a",
               "image": ["pseudo_encode1", "pseudo_encode2"],
               "name": ["01.jpg", "02.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1a",
               "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
               "name": ["01.jpg", "02.jpg", "03.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1_a",
               "image": ["pseudo_encode1", "pseudo_encode2", "pseudo_encode3"],
               "name": ["01.jpg", "02.jpg", "03.jpg"],
               "size": [[10, 10, 3], [20, 15, 3], [50, 55, 3]]},
              {"user_id": "1_a",
               "image": ["pseudo_encode4"],
               "name": ["04.jpg"],
               "size": [[30, 10, 3]]},
              {"user_id": "1_a",
               "image": ["pseudo_encode5", "pseudo_encode6"],
               "name": ["05.jpg", "06.jpg"],
               "size": [[10, 10, 1], [20, 15, 3]]}]
    for info in u_info:
        post_images(info)
    return None


def post_process_images(info):
    """The client function of posting processed images.

    Args:
        info (dict): The dictionary of image information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/process",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)
    return None


def process_test_imageset():
    """Create a pseudo-lists of processing image information to
    add into the server and database.

    The pseudo-lists of image information contain errors of:
    (1) Wrong dictionary key
    (2) Wrong operation index
    (2) Wrong format of image
    (3) Wrong format of image name
    (4) Wrong format of image size
    (5) The lengths of images, their names and their size are not equal
    (6) Not existed id
    Ultimately three valid processing image information will be added into
    the database with the id of "1_a".

    Returns:
        None
    """
    root = "/Users/liangyu/Downloads/Docs/BME/BME547/Lecture/" \
           "image_processer/101_ObjectCategories/bonsai"
    path = [root+'/image_0014.jpg', root+'/image_0015.jpg',
            root+'/image_0016.jpg', root+'/image_0017.jpg',
            root+'/image_0018.jpg', root+'/image_0019.jpg',
            root+'/image_0020.jpg', root+'/image_0021.jpg',
            root+'/image_0022.jpg']
    images_encoded = []
    size = []
    name = []
    for i in path:
        img = io.imread(i)
        img_name = os.path.basename(i)
        img_b64, img_size = image_to_b64(img)
        size.append(list(img_size))
        name.append(img_name)
        images_encoded.append(str(img_b64))
    images = []
    for i in path[0:3]:
        img = io.imread(i)
        images.append(img.tolist())
    u_info = [{"userid": "1_a", "operation": 0,
               "raw_img": images_encoded[0:3],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 10,
               "raw_img": images_encoded[0:3],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 0,
               "raw_img": images[0:3],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 0,
               "raw_img": images_encoded[0:3],
               "size": size[0:3], "name": ["1", "3jpg", "png"]},
              {"user_id": "1_a", "operation": 0,
               "raw_img": images_encoded[0:3],
               "size": [200, 300, 3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 0,
               "raw_img": images_encoded[0:2],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "none", "operation": 0,
               "raw_img": images_encoded[0:3],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 0,
               "raw_img": images_encoded[0:3],
               "size": size[0:3], "name": name[0:3]},
              {"user_id": "1_a", "operation": 1,
               "raw_img": images_encoded[3:6],
               "size": size[3:6], "name": name[3:6]},
              {"user_id": "1_a", "operation": 3,
               "raw_img": images_encoded[6:9],
               "size": size[6:9], "name": name[6:9]}]
    for info in u_info:
        post_process_images(info)
    return None


if __name__ == '__main__':
    test_add_patients()
    request_check_id()
    test_add_images()
    process_test_imageset()
