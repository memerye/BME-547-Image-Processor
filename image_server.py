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
    for key in user_info.keys():
        if key not in expected_keys:
            return False
    return True


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
