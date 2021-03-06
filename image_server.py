# image_server.py
from flask import Flask, jsonify, request
import re
import logging
from pymodm import connect
import initial_database
from image_processing import ImageProcessing
from en_de_code import image_to_b64, b64_to_image
from datetime import datetime

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
        image_info (dict): the posted image data.

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


def validate_images(images):
    """Validate the format of the encoded images as strings

    Args:
        images (list): the posted encoded image data.

    Returns:
        bool: True if the images are all valid;
        False if it contains wrong format of images.
    """
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


def validate_image_names(names):
    """Validate the format of the image names as "name.type".
    e.g. "01.jpg", but not "01jpg"

    Args:
        names (list): the posted image names.

    Returns:
        bool: True if the names are all valid;
        False if it contains wrong format of names.
    """
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


def validate_size(size):
    """Validate the format of the size of the images.

    The "size" stores all of the images' size as a list.
    The numbers of the size should all be int.
    e.g. [[200, 300, 3], [100, 150, 1]].

    Args:
        size (list): the posted image size.

    Returns:
        bool: True if the names are all valid;
        False if it contains wrong format of names.
    """
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


def validate_data_length(image, name, size):
    """Validate the total lengths of the images, their names and their sizes.

    The total lengths of the images, their names and their size should
    always be equal.

    Args:
        image (list): the posted image data.
        name (list): the posted image names.
        size (list): the posted image size.

    Returns:
        bool: True if the length are all equal;
        False if they have different length.
    """
    try:
        assert len(image) == len(name) == len(size)
    except AssertionError:
        return False
    else:
        return True


@app.route("/api/upload_images", methods=["POST"])
def add_images():
    """Post images to the database

    Before posting new images to database, the keys and the
    values in the posted json should all be validated first.
    If there is anything invalid in the posted json, the server
    will return error status codes with reasons.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    good_keys = validate_image_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    images = indata["image"]
    if validate_images(images) is False:
        return "Please upload the encoded images!", 400
    names = indata["name"]
    if validate_image_names(names) is False:
        return "Please upload the valid image names!", 400
    size = indata["size"]
    if validate_size(size) is False:
        return "The type of image size is not valid!", 400
    if validate_data_length(images, names, size) is False:
        return "The total lengths of the images, their names and" \
               "their size should always be equal.", 400
    u_id = indata["user_id"]
    if initial_database.validate_existing_id(u_id):
        initial_database.add_original_image_to_db(indata)
        num = len(indata["image"])
        logging.info("* ID {} has uploaded {} images."
                     .format(u_id, num))
        return "Valid image data!"
    else:
        return "The user doesn't exist!", 400


def validate_process_keys(process_info):
    """Validate the image processing keys

    Args:
        process_info (dict): The posted image processing data

    Returns:
        bool: True if the keys are all valid;
        False if it contains wrong keys.
    """
    expected_keys = ["user_id", "operation",
                     "raw_img", "size", "name"]
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


def validate_operation(process_info):
    """Validation the index of the operation.

    Args:
        process_info (dict): The posted image processing data.

    Returns:
        False: if the operation is not valid;
        int: if the operation is valid.
    """
    operation = process_info["operation"]
    expected_op = [0, 1, 2, 3]
    try:
        float(operation)
    except ValueError:
        return False
    try:
        assert float(operation).is_integer()
    except AssertionError:
        return False
    else:
        op = int(operation)
        if op not in expected_op:
            return False
        else:
            return op


def process_image(img, operation):
    """Process the image with specific operation.

    The operation are encoded as:
    0 - Histogram Equalization
    1 - Contrast Stretching
    2 - Log Compression
    3 - Invert Image

    Args:
        img (ndarray): The posted processing image(s);
        operation (int): The operation index.

    Returns:
        ndarray: The processed images;
        float: The time needed to processing this image.
    """
    I = ImageProcessing(img)
    if operation == 0:
        processed_img, run_time = I.histeq()
    elif operation == 1:
        processed_img, run_time = I.constr()
    elif operation == 2:
        processed_img, run_time = I.logcom()
    elif operation == 3:
        processed_img, run_time = I.invert()
    else:
        return False
    return processed_img, run_time


@app.route("/api/process", methods=["POST"])
def img_process():
    """Post the image information related to one processing

    Before posting new processed images to database, the keys and
    the values in the posted json should all be validated first.
    If there is anything invalid in the posted json, the server
    will return error status codes with reasons. The ultimately
    processed images will be saved into the database.

    Returns:
        string: message to indicate the status of the server.
    """
    indata = request.get_json()
    good_keys = validate_process_keys(indata)
    if good_keys is False:
        return "The dictionary keys are not correct.", 400
    op = validate_operation(indata)
    if op is False:
        return "This operation doesn't exist!", 400
    raw_images = indata["raw_img"]
    if validate_images(raw_images) is False:
        return "Please upload the encoded images!", 400
    names = indata["name"]
    if validate_image_names(names) is False:
        return "Please upload the valid image names!", 400
    size = indata["size"]
    if validate_size(size) is False:
        return "The type of image size is not valid!", 400
    if validate_data_length(raw_images, names, size) is False:
        return "The total lengths of the images, their names and" \
               "their size should always be equal.", 400
    u_id = validate_id(indata)
    indata["user_id"] = u_id
    u_size = indata["size"]
    indata["processed_img"] = []
    indata["run_time"] = []
    if initial_database.validate_existing_id(u_id):
        for img_i, size_i in zip(raw_images, u_size):
            size_i_tuple = tuple(size_i)
            img = b64_to_image(img_i, size_i_tuple)
            processed_img, run_time = process_image(img, op)
            processed_img_b64, _ = image_to_b64(processed_img)
            indata["processed_img"].append(processed_img_b64)
            indata["run_time"].append(run_time)
        indata["processed_time"] = str(datetime.now())
        num = len(indata["processed_img"])
        indata["up_time"] = initial_database.get_upload_time(u_id, num)
        initial_database.add_processed_image_to_db(indata)
        logging.info("* ID {} has processed {} images."
                     .format(u_id, num))
        return "Success process!"
    else:
        return "The user doesn't exist!", 400


@app.route("/api/user_info/<user_id>", methods=["GET"])
def user_info(user_id):
    """The client function of getting user information.

    User information includes:
    (1) user id
    (2) how many images have been uploaded
    (3) the total number of times of the various image processing steps.
    If the user id doesn't exist, the server will return error
    status codes with reasons.

    Args:
        user_id (string): The user id

    Returns:
        False if no existing patient.
        json: a json message containing the information
    """
    if initial_database.validate_existing_id(user_id):
        data = initial_database.get_user_info(user_id)
        return jsonify(data)
    else:
        return "The user doesn't exist!", 400


@app.route("/api/history_info/<user_id>", methods=["GET"])
def history_info(user_id):
    """The client function of getting user history operation list.

    User information includes:
    (1) user id
    (2) the indexes of the operation
    (3) the timestamp when user process the imaeg(s)
    (4) the operation name
    (5) the image(s) name
    If the user id doesn't exist, the server will return error
    status codes with reasons.

    Args:
        user_id (string): The user id

    Returns:
        False if no existing patient.
        json: a json message containing the information
    """
    if initial_database.validate_existing_id(user_id):
        data = initial_database.get_history_info(user_id)
        return jsonify(data)
    else:
        return "The user doesn't exist!", 400


@app.route("/api/history_info/<user_id>/<num>", methods=["GET"])
def one_history_info(user_id, num):
    """The client function of retrieve one of the history information

    User information includes:
    (1) user id
    (2) the index of the operation
    (3) uploaded time of the image(s)
    (4) the operation name
    (5) the size of the image(s)
    (6) the CPU running time for each image processing
    (7) the image name(s)
    (8) the raw image(s)
    (9) the processed image(s)
    If the user id doesn't exist, the server will return error
    status codes with reasons.

    Args:
        user_id (string): The user id
        num (int): The index of the operation

    Returns:
        False if no existing patient.
        json: a json message containing the information
    """
    if initial_database.validate_existing_id(user_id):
        data = initial_database.retrieve_history_info(user_id, num)
        return jsonify(data)
    else:
        return "The user doesn't exist!", 400


@app.route("/api/most_recent_processed_image/<user_id>", methods=["GET"])
def recent_process_images(user_id):
    """The client function of processing the images that just uploaded

    User information includes:
    (1) user id
    (2) uploaded time of the image(s)
    (3) the operation name
    (4) the size of the image(s)
    (5) the CPU running time for each image processing
    (6) the image name(s)
    (7) the raw image(s)
    (8) the processed image(s)
    If the user id doesn't exist, the server will return error
    status codes with reasons.

    Args:
        user_id (string): The user id

    Returns:
        False if no existing patient.
        json: a json message containing the information
    """
    if initial_database.validate_existing_id(user_id):
        data = initial_database.get_rec_pro_img(user_id)
        return jsonify(data)
    else:
        return "The user doesn't exist!", 400


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
