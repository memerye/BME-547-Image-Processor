# database.py
from datetime import datetime
from pymodm import MongoModel, fields

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


class ImageUser(MongoModel):
    user_id = fields.CharField(primary_key=True)
    created_timestamp = fields.CharField()
    metrics = fields.DictField()
    images = fields.DictField()
    processed = fields.DictField()


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
