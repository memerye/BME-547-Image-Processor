# image_client.py
import requests
from skimage import io
from en_de_code import image_to_b64, b64_to_image


def post_user_id(info):
    """The client function of posting a new user.

    Args:
        info (dict): the dictionary of patient's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/new_user",
                      json=info)
    print(r)
    print(r.text)
    print(r.status_code)


def test_add_patients():
    """Create a pseudo-list of patients information to
    add into the server and database.

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


if __name__ == '__main__':
    test_add_patients()
