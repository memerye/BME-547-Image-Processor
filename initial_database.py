# database.py
from datetime import datetime
from pymodm import MongoModel, fields
from pymodm import connect


# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def init_mongodb():
    connect("mongodb+srv://python_code:bme547final\
        @bme547-reiux.mongodb.net/test?retryWrites=true&w=majority")


class ImageUser(MongoModel):
    user_id = fields.CharField(primary_key=True)
    created_timestamp = fields.CharField()
    metrics = fields.DictField()
    images = fields.DictField()
    processed = fields.DictField()


def validate_existing_id(u_id):
    """Validate the existence of the user id in the database.
    Args:
        u_id (string): the patient id.
    Returns:
        bool: False if the id doesn't exist in the database;
        True if the id has been registered in the database.
    """
    id_list = []
    for u in ImageUser.objects.raw({}):
        id_list.append(u.user_id)
    if u_id in id_list:
        return True
    else:
        return False


def add_new_user_to_db(user_info):
    u_id = user_info["user_id"]
    u_time = str(datetime.now())
    key_list_metrics = ("img_num", "histeq", "constr", "logcom", "invert")
    key_list_images = ("image", "name", "size", "time")
    key_list_process = ("num", "timestamp", "operation", "size",
                        "run_time", "name", "raw_img", "processed_img")
    u = ImageUser(user_id=u_id,
                  created_timestamp=u_time,
                  metrics=dict.fromkeys(key_list_metrics, []),
                  images=dict.fromkeys(key_list_images, []),
                  processed=dict.fromkeys(key_list_process, []))
    u.save()
    return None


def add_original_image_to_db(u_img):
    u_id = u_img["user_id"]
    image_list = u_img["image"]
    name_list = u_img["name"]
    size_list = u_img["size"]
    imageuser = ImageUser.objects.raw({"_id": u_id}).first()
    for single_img in image_list:
        imageuser.images["image"].append(single_img)
        imageuser.images["time"].append(str(datetime.now()))
    for name in name_list:
        imageuser.images["name"].append(name)
    for size in size_list:
        imageuser.images["size"].append(size)
    imageuser.metrics["img_num"] = [len(image_list)]
    imageuser.save()
    return None


if __name__ == '__main__':
    init_mongodb()
