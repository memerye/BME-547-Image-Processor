# test_initial_database.py
import pytest
from pymodm import connect


@pytest.mark.parametrize("user_info, u_id", [
    ({"user_id": "Bob1"}, "Bob1"),
    ({"user_id": "Jenny2"}, "Jenny2")
])
def test_add_new_user_to_db(user_info, u_id):
    from initial_database import add_new_user_to_db, ImageUser
    connect("mongodb+srv://python_code:bme547final@bme547-reiux."
            "mongodb.net/test?retryWrites=true&w=majority")
    add_new_user_to_db(user_info)
    u = ImageUser.objects.raw({"_id": u_id}).first()
    assert u_id == u.user_id


@pytest.mark.parametrize("u_id, expected", [
    ("Bob1", True),
    ("Who3", False)
])
def test_validate_existing_id(u_id, expected):
    from initial_database import validate_existing_id
    result = validate_existing_id(u_id)
    assert result == expected


def test_add_original_image_to_db():
    test_input = {"user_id": "Bob1", "image": ["abc", "cd"],
                  "name": ["abc.jpg", "cd.jpg"],
                  "size": [[200, 200, 3], [200, 200, 3]],
                  "time": ["2019 - 12 - 07 17: 12: 09.164933",
                           "2019 - 12 - 08 17: 12: 09.164933"]}
    from initial_database import add_original_image_to_db, ImageUser
    add_original_image_to_db(test_input)
    u = ImageUser.objects.raw({"_id": "Bob1"}).first()
    expected = ["abc", "cd"]
    assert expected == u.images["image"]
