# image_server.py
from flask import Flask, jsonify, request
import re
import logging
from pymodm import connect
import initial_database

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)


def validate_user_keys(user_info):
    """Validate the keys when posting a new user.

    The keys of this posted user information should
    only contain "user_id", otherwise it would be
    regarded as wrong information.

    Args:
        user_info (dict): the posted user id.

    Returns:
        bool: True if the keys are all valid;
        False if it contains wrong keys.
    """
    expected_keys = ["user_id"]
    flag = 0
    for key in user_info.keys():
        if key not in expected_keys:
            return False
        else:
            flag = flag + 1
    if flag == 1:
        return True
    else:
        return False


def validate_id(user_info):
    """Validate the user id.

    The user id can be the combination of the letters, numbers and "_".
    The whitespace in the user id would be removed.

    Args:
        user_info (dict): the posted user id.

    Returns:
        False: if the id is not valid;
        string: if the id is valid.
    """
    u_id = user_info["user_id"]
    try:
        regex = "^[A-Za-z0-9-_ ]*$"
        assert re.match(regex, u_id)
    except AssertionError:
        return False
    except TypeError:
        return False
    u_id = u_id.replace(" ", "")
    return u_id


@app.route("/api/new_user", methods=["POST"])
def add_user_id():
    """Post a new user to the database.

    Before posting a new user to database, the keys and the
    values in the posted json should all be validated first.
    If this is the first time that this user logs into the server,
    Then the new user will be registered in the server as well as
    saved in the database. The "user_id" is the primary key for
    each user, so it should be unique for each user. If there is
    anything invalid in the posted json, the server will return
    error status codes with reasons.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    good_keys = validate_user_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    u_id = validate_id(indata)
    indata["user_id"] = u_id
    if u_id is False:
        return "Please enter a valid ID.", 400
    if initial_database.validate_existing_id(u_id):
        return "The user has logged in."
    else:
        initial_database.add_new_user_to_db(indata)
        logging.info("* ID {} has been registered in server."
                     .format(u_id))
        return "The user has been registered and logged in."


@app.route("/api/check_id/<user_id>", methods=["GET"])
def check_user_id(user_id):
    """Get the message if this id exists in the database.

    Args:
        user_id (string): The id of this user

    Returns:
        json: The bool variable of the existence of this id
    """
    result = initial_database.validate_existing_id(user_id)
    flag = {"result": result}
    return jsonify(flag)


def validate_image_keys(image_info):
    """Validate the keys when posting images

    Args:
        image_info(dict): the posted image data.

    Returns:
        bool: True if the keys are all valid;
        False if it contains wrong keys.
    """
    expected_keys = ["user_id", "image", "name", "size"]
    flag = 0
    for key in image_info.keys():
        if key not in expected_keys:
            return False
        else:
            flag = flag + 1
    if flag == 4:
        return True
    else:
        return False


def validate_images(image_info):
    """Validate the format of the encoded images as strings

    Args:
        image_info(dict): the posted image data.

    Returns:
        bool: True if the images are all valid;
        False if it contains wrong format of images.
    """
    images = image_info["image"]
    try:
        assert type(images) == list
    except AssertionError:
        return False
    for i in images:
        try:
            assert type(i) == str
        except AssertionError:
            return False
    return True


def validate_image_names(image_info):
    """Validate the format of the image names as "name.type".
    e.g. "01.jpg", but not "01jpg"

    Args:
        image_info(dict): the posted image data.

    Returns:
        bool: True if the names are all valid;
        False if it contains wrong format of names.
    """
    names = image_info["name"]
    try:
        assert type(names) == list
    except AssertionError:
        return False
    for n in names:
        try:
            assert type(n) == str
            assert "." in n
        except AssertionError:
            return False
    return True


def validate_size(image_info):
    """Validate the format of the size of the images.

    The "size" stores all of the images' size as a list.
    The numbers of the size should all be int.
    e.g. [[200, 300, 3], [100, 150, 1]].

    Args:
        image_info(dict): the posted image data.

    Returns:
        bool: True if the names are all valid;
        False if it contains wrong format of names.
    """
    size = image_info["size"]
    try:
        assert type(size) == list
    except AssertionError:
        return False
    for a_size in size:
        try:
            assert type(a_size) == list
            assert len(a_size) == 2 or len(a_size) == 3
        except AssertionError:
            return False
        for i in a_size:
            try:
                assert type(i) == int
            except AssertionError:
                return False
    return True


def validate_data_length(image_info):
    """Validate the total lengths of the images, their names and their size.

    The total lengths of the images, their names and their size should
    always be equal.

    Args:
        image_info(dict): the posted image data.

    Returns:
        bool: True if the length are all equal;
        False if they have different length.
    """
    try:
        assert len(image_info["image"]) == \
               len(image_info["name"]) == len(image_info["size"])
    except AssertionError:
        return False
    else:
        return True


@app.route("/api/upload_images", methods=["POST"])
def add_images():
    indata = request.get_json()
    good_keys = validate_image_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    if validate_images(indata) is False:
        return "Please upload the encoded images!", 400
    if validate_image_names(indata) is False:
        return "Please upload the valid image names!", 400
    if validate_size(indata) is False:
        return "The type of image size is not valid!", 400
    if validate_data_length(indata) is False:
        return "The total lengths of the images, their names and" \
               "their size should always be equal.", 400
    u_id = indata["user_id"]
    if initial_database.validate_existing_id(u_id):
        initial_database.add_original_image_to_db(indata)
        #############################################
        num = len(indata["image"])
        logging.info("* ID {} has uploaded {} images."
                     .format(u_id, num))
        #############################################
        return "Valid image data!"
    else:
        return "The user doesn't exist!", 400


def validate_process_keys(process_info):
    expected_keys = ["user_id", "operation", "raw_img", "size", "name"]
    flag = 0
    for key in process_info.keys():
        if key not in expected_keys:
            return False
        else:
            flag = flag+1
    if flag == 5:
        return True
    else:
        return False


def init_server():
    """Initialize the logging configuration and database connection.

    Returns:
        None.
    """
    logging.basicConfig(filename='image_server.log',
                        level=logging.INFO,
                        filemode='w')
    connect("mongodb+srv://python_code:bme547final@bme547-reiux."
            "mongodb.net/test?retryWrites=true&w=majority")
    return None


if __name__ == "__main__":
    init_server()
    app.run()
