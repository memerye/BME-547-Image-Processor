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
    test_input = {"user_id": "Bob1",
                  "image": ["abc", "cd"],
                  "name": ["abc.jpg", "cd.jpg"],
                  "size": [[200, 200, 3], [200, 200, 3]]}
    from initial_database import add_original_image_to_db, ImageUser
    add_original_image_to_db(test_input)
    u = ImageUser.objects.raw({"_id": "Bob1"}).first()
    expected_image = ["abc", "cd"]
    expected_name = ["abc.jpg", "cd.jpg"]
    expected_size = [[200, 200, 3], [200, 200, 3]]
    assert expected_image == u.images["image"]
    assert expected_name == u.images["name"]
    assert expected_size == u.images["size"]


def test_add_processed_image_to_db():
    test_input = {"user_id": "Bob1",
                  "operation": 0,
                  "up_time": ["13:10", "13:11"],
                  "size": [[200, 200, 3], [200, 200, 3]],
                  "run_time": [0.1, 0.2],
                  "name": ["aa.jpg", "bb.jpg"],
                  "raw_img": ["abc", "cd"],
                  "processed_img": ["cc", "dd"],
                  "processed_time": ["14:00", "14:01"]}
    from initial_database import add_processed_image_to_db, ImageUser
    add_processed_image_to_db(test_input)
    u = ImageUser.objects.raw({"_id": "Bob1"}).first()
    expected_operation = [0]
    expected_up_time = [["13:10", "13:11"]]
    expected_size = [[[200, 200, 3], [200, 200, 3]]]
    expected_run_time = [[0.1, 0.2]]
    expected_name = [["aa.jpg", "bb.jpg"]]
    expected_raw_img = [["abc", "cd"]]
    expected_processed_img = [["cc", "dd"]]
    assert expected_operation == u.processed["operation"]
    assert expected_up_time == u.processed["up_time"]
    assert expected_size == u.processed["size"]
    assert expected_run_time == u.processed["run_time"]
    assert expected_name == u.processed["name"]
    assert expected_raw_img == u.processed["raw_img"]
    assert expected_processed_img == u.processed["processed_img"]


def test_get_rec_pro_img():
    test_input = "Bob1"
    from initial_database import get_rec_pro_img
    rec_pro = get_rec_pro_img(test_input)
    expected = {"user_id": "Bob1",
                "up_time": ["13:10", "13:11"],
                "operation": 0,
                "size": [[200, 200, 3], [200, 200, 3]],
                "run_time": [0.1, 0.2],
                "name": ['aa.jpg', 'bb.jpg'],
                "raw_img": ['abc', 'cd'],
                "processed_img": ['cc', 'dd']}
    assert expected == rec_pro


def test_get_user_info():
    from initial_database import get_user_info
    result = get_user_info("Bob1")
    expected = {"user_id": "Bob1",
                "img_num": 2,
                "histeq": 1,
                "constr": 0,
                "logcom": 0,
                "invert": 0}
    assert result["user_id"] == expected["user_id"]
    assert result["img_num"] == expected["img_num"]
    assert result["histeq"] == expected["histeq"]
    assert result["constr"] == expected["constr"]
    assert result["logcom"] == expected["logcom"]
    assert result["invert"] == expected["invert"]


def test_get_history_info():
    from initial_database import get_history_info
    result = get_history_info("Bob1")
    expected = {"user_id": "Bob1",
                "num": [1],
                "processed_time": [["14:00", "14:01"]],
                "operation": [0],
                "name": [["aa.jpg", "bb.jpg"]]}

    assert result == expected


def test_retrieve_history_info():
    from initial_database import retrieve_history_info
    result = retrieve_history_info("Bob1", 1)
    expected = {"user_id": "Bob1",
                "num": 1,
                "up_time": ["13:10", "13:11"],
                "operation": 0,
                "size": [[200, 200, 3], [200, 200, 3]],
                "run_time": [0.1, 0.2],
                "name": ["aa.jpg", "bb.jpg"],
                "raw_img": ["abc", "cd"],
                "processed_img": ["cc", "dd"]}
    assert result == expected
