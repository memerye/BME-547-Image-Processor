import requests
from skimage import io
from en_de_code import image_to_b64, b64_to_image
import os


def request_check_id(ids):
    r = requests.get("http://127.0.0.1:5000/api/check_id/{}".format(ids))
    answer = r.json()
    return answer["result"]


def post_user_id(info):
    r = requests.post("http://127.0.0.1:5000/api/new_user",
                      json=info)
    return None


def post_img_GUI(info):
    r = requests.post("http://127.0.0.1:5000/api/upload_images",
                      json=info)
    return None


def request_user_info(ids):
    r = requests.get("http://127.0.0.1:5000/api/user_info/{}".format(ids))
    answer = r.json()
    return answer


def post_process_opt(info):
    """The client function of posting processed images.

    Args:
        info (dict): The dictionary of image information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/process",
                      json=info)
    return None


def request_history_info(ids):
    r = requests.get("http://127.0.0.1:5000/api/history_info/{}"
                     .format(ids))
    answer = r.json()
    print(answer)
    return answer


def request_one_history_info(ids, num):
    r = requests.get("http://127.0.0.1:5000/api/history_info/{}/{}"
                     .format(ids, num))
    answer = r.json()
    print(answer)
    return answer


def request_recent_process_images(ids):
    """The client function of processing the images that just uploaded

     User information includes:
     (1) user id
     (2) uploaded time of the image(s)
     (3) the operation name
     (4) the size of the image(s)
     (5) the CPU running time for each image processing
     (6) the image name(s)
     (7) the raw image(s)
     (8) the processed image(s)
     While user "08563" is not in the database,
     and we can get the expected message from server.

     The results will be printed out.

     Returns:
         None
     """
    r = requests.get("http://127.0.0.1:5000/api/"
                     "most_recent_processed_image/{}".format(ids))
    answer = r.json()
    print(answer)
    return answer


if __name__ == '__main__':
    a = request_recent_process_images("1_a")
