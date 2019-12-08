# image_client.py
import requests
from skimage import io
from en_de_code import image_to_b64, b64_to_image


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


if __name__ == '__main__':
    test_add_patients()
    request_check_id()
