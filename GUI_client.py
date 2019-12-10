import requests
from skimage import io
from en_de_code import image_to_b64, b64_to_image
import os


def request_check_id(x):
    r = requests.get("http://127.0.0.1:5000/api/check_id/{}".format(x))
    answer = r.json()
    # print(answer["result"])
    return answer["result"]


def post_user_id(info):
    r = requests.post("http://127.0.0.1:5000/api/new_user",
                      json=info)
    return None


def post_img_GUI(info):
    r = requests.post("http://127.0.0.1:5000/api/upload_images",
                      json=info)
    return None


def post_process_opt(info):
    r = requests.post("http://127.0.0.1:5000/api/process",
                      json=info)
    return None


def request_user_info(ids):
    r = requests.get("http://127.0.0.1:5000/api/user_info/{}".format(ids))
    answer = r.json()
    return answer


def request_history_info(ids):
    r = requests.get("http://127.0.0.1:5000/api/history_info/{}"
                     .format(ids))
    answer = r.json()
    return answer


if __name__ == '__main__':
    request_check_id()
