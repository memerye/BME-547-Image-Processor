# database.py
from datetime import datetime
from pymodm import connect, MongoModel, fields
import pymongo
from pymongo import MongoClient
import urllib.parse


# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def init_mongodb():
    connect("mongodb+srv://python_code:bme547final@bme547-reiux.mongodb.net/test?retryWrites=true&w=majority")


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
    """Add new user to database
    Arg:
        user_info (dict): the user information
    Returns:

    """
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
    u_metric = u_img["metrics"]
    u_images = u_img["images"]
    image_list = u_images["image"]
    name_list = u_images["name"]
    size_list = u_images["size"]
    time_list = u_images["time"]
    imageuser = ImageUser.objects.raw({"user_id": u_id})
    for single_img in image_list:
        imageuser.images["image"].append(single_img)
    for name in name_list:
        imageuser.images["name"].append(name)
    for size in size_list:
        imageuser.images["size"].append(size)
    for time in time_list:
        imageuser.images["time"].append(time)
    imageuser.metrics["num"] = u_metric["img_num"] + imageuser.metrics["num"]
    imageuser.save()
    return None


def add_processed_image_to_db(u_processed):
    u_id = u_processed["user_id"]
    u_pro = u_processed["process"]
    #"num", "timestamp", "operation" , "size",
    # "run_time", "name", "raw_img", "processed_img"
    # key_list_metrics = ("img_num", "histeq", "constr", "logcom", "invert")
    # key_list_process = ("num", "timestamp", "operation", "size",
    #                     "run_time", "name", "raw_img", "processed_img")
#     This route is called to let the user process the selected image with specific operation. The operation is encoded as 0, 1, 2, 3.
# 0: Histogram Equalization
# 1: Contrast Stretching
# 2: Log Compression
# 3: Invert Image
    raw_list = u_pro["raw_img"]
    name_list = u_pro["name"]
    processed_list = u_pro["processed_img"]
    time_list = u_pro["run_time"]
    size_list = u_pro["size"]
    oper_num_list = u_pro["operation"]
    stamp_list = u_pro["timestamp"]
    index = u_pro["num"]
    imageuser = ImageUser.objects.raw({"user_id": u_id})
#add new data to process 
    for single_img in image_list:
        imageuser.proc["image"].append(single_img)
    for name in name_list:
        imageuser.images["name"].append(name)
    for size in size_list:
        imageuser.images["size"].append(size)
    for time in time_list:
        imageuser.images["time"].append(time)
    imageuser



    return


if __name__ == '__main__':
    init_mongodb()
    user_info = {"user_id": "test1"}
    add_new_user_to_db(user_info)
    find({"user_id": "test1"})
