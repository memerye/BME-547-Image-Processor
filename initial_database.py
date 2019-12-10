# database.py
from datetime import datetime
from pymodm import MongoModel, fields
from pymodm import connect
import pymongo
# Ignore warnings
import warnings

warnings.filterwarnings("ignore")


def init_mongodb():
    """Connect the mongodb
    Args:
        None
    Returns:
        None
    """
    connect("mongodb+srv://python_code:bme547final\
        @bme547-reiux.mongodb.net/test?retryWrites=true&w=majority")


class ImageUser(MongoModel):
    user_id = fields.CharField(primary_key=True)
    created_timestamp = fields.CharField()
    metrics = fields.DictField()
    images = fields.DictField()
    processed = fields.DictField()


def add_new_user_to_db(user_info):
    """Add new user to the database and initialize user info in database
    Args:
        u_info (dict): a dictionary containing u_id
    Returns:
        None
    """
    u_id = user_info["user_id"]
    u_time = str(datetime.now())
    key_list_metrics = ("img_num", "histeq", "constr", "logcom", "invert")
    key_list_images = ("image", "name", "size", "time")
    key_list_processed = ("num", "timestamp", "operation", "size",
                          "run_time", "name", "raw_img", "processed_img")
    u = ImageUser(user_id=u_id,
                  created_timestamp=u_time,
                  metrics=dict.fromkeys(key_list_metrics, [0]),
                  images=dict.fromkeys(key_list_images, []),
                  processed=dict.fromkeys(key_list_processed, []))
    u.save()
    return None


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


def add_original_image_to_db(u_img):
    """Add original image to the database as a dict.
    Args:
        u_img (dict): a dictionary containing original image info and u_id
    Returns:
        None
    """
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
    img_num = imageuser.metrics["img_num"][0]
    imageuser.metrics["img_num"][0] = img_num + len(image_list)
    imageuser.save()
    return None


def add_processed_image_to_db(u_pro):
    """Add processed image to database as a dict.
    Args:
        u_pro (dict): a dictionary containing
        the u_id and processed image info.
    Returns:
        None
    """
    u_id = u_pro["user_id"]
    oper_num = u_pro["operation"]
    size = u_pro["size"]
    run = u_pro["run_time"]
    name = u_pro["name"]
    raw = u_pro["raw_img"]
    pro = u_pro["processed_img"]
    imageuser = ImageUser.objects.raw({"_id": u_id}).first()
    if len(imageuser.processed["num"]):
        cur_ind = imageuser.processed["num"][-1]
    else:
        cur_ind = 0
    imageuser.processed["operation"].append(oper_num)
    cur_ind += 1
    imageuser.processed["num"].append(cur_ind)
    imageuser.processed["size"].append(size)
    imageuser.processed["run_time"].append(run)
    imageuser.processed["name"].append(name)
    imageuser.processed["raw_img"].append(raw)
    imageuser.processed["processed_img"].append(pro)
    imageuser.processed["timestamp"].append(str(datetime.now()))
    if oper_num == 0:
        imageuser.metrics["histeq"][0] = imageuser.metrics["histeq"][0] + 1
    elif oper_num == 1:
        imageuser.metrics["constr"][0] = imageuser.metrics["constr"][0] + 1
    elif oper_num == 2:
        imageuser.metrics["logcom"][0] = imageuser.metrics["logcom"][0] + 1
    elif oper_num == 3:
        imageuser.metrics["invert"][0] = imageuser.metrics["invert"][0] + 1
    imageuser.save()
    return None


def get_rec_pro_img(u_id):
    """Get most recent processed image and output as a dictionary
    Args:
        u_id: user id string variable
    Returns:
        A dictionary containing searching information
    """
    imageuser = ImageUser.objects.raw({"_id": u_id}).first()
    rec_dict = {}
    rec_dict["user_id"] = u_id
    rec_dict["timestamp"] = imageuser.processed["timestamp"][-1]
    rec_dict["operation"] = imageuser.processed["operation"][-1]
    rec_dict["size"] = imageuser.processed["size"][-1]
    rec_dict["run_time"] = imageuser.processed["run_time"][-1]
    rec_dict["name"] = imageuser.processed["name"][-1]
    rec_dict["raw_img"] = imageuser.processed["raw_img"][-1]
    rec_dict["processed_img"] = imageuser.processed["processed_img"][-1]
    return rec_dict


def get_user_info(user_id):
    u_db = ImageUser.objects.raw({"_id": user_id}).first()
    user_info = {"user_id": user_id,
                 "create_time": u_db.created_timestamp,
                 "img_num": u_db.metrics["img_num"][0],
                 "histeq": u_db.metrics["histeq"][0],
                 "constr": u_db.metrics["constr"][0],
                 "logcom": u_db.metrics["logcom"][0],
                 "invert": u_db.metrics["invert"][0]}
    return user_info


def get_history_info(user_id):
    u_db = ImageUser.objects.raw({"_id": user_id}).first()
    history = {"user_id": user_id,
               "num": u_db.processed["num"],
               "timestamp": u_db.processed["timestamp"],
               "operation": u_db.processed["operation"],
               "name": u_db.processed["name"]}
    return history


def retrieve_history_info(user_id, num):
    u_db = ImageUser.objects.raw({"_id": user_id}).first()
    num = int(num)
    history = {"user_id": user_id,
               "num": num,
               "timestamp": u_db.processed["timestamp"][num-1],
               "operation": u_db.processed["operation"][num-1],
               "size": u_db.processed["size"][num-1],
               "run_time": u_db.processed["run_time"][num-1],
               "name": u_db.processed["name"][num-1],
               "raw_img": u_db.processed["raw_img"][num-1],
               "processed_img": u_db.processed["processed_img"][num-1]}
    return history


if __name__ == '__main__':
    init_mongodb()
