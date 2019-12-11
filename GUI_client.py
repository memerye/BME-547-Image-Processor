import requests


def request_check_id(ids):
    """The client function of checking the existence of this id.

    Args:
        ids (string): the user id.

    Returns:
        bool: The existence of this id.
    """
    r = requests.get("http://127.0.0.1:5000/api/check_id/{}".format(ids))
    answer = r.json()
    return answer["result"]


def post_user_id(info):
    """The client function of posting a new user.

    Args:
        info (dict): the dictionary of user's information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/new_user",
                      json=info)
    return None


def post_img_GUI(info):
    """The client function of posting images.

    Args:
        info (dict): The dictionary of image information.

    Returns:
        None
    """
    r = requests.post("http://127.0.0.1:5000/api/upload_images",
                      json=info)
    return None


def request_user_info(ids):
    """The client function of getting user information.

    User information includes:
    (1) user id
    (2) how many images have been uploaded
    (3) the total number of times of the various image processing steps.

    Args:
        ids (string): the user id

    Returns:
        json: return the user information to client.
    """
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
    """The client function of getting user history operation list.

    User information includes:
    (1) user id
    (2) the indexes of the operation
    (3) the timestamp when user process the imaeg(s)
    (4) the operation name
    (5) the image(s) name

    Args:
        ids (string): the user id

    Returns:
        json: return the history information to client.
    """
    r = requests.get("http://127.0.0.1:5000/api/history_info/{}"
                     .format(ids))
    answer = r.json()
    print(answer)
    return answer


def request_one_history_info(ids, num):
    """The client function of retrieve one of the history information

     User information includes:
     (1) user id
     (2) the index of the operation
     (3) uploaded time of the image(s)
     (4) the operation name
     (5) the size of the image(s)
     (6) the CPU running time for each image processing
     (7) the image name(s)
     (8) the raw image(s)
     (9) the processed image(s)

    Args:
        ids (string): the user id
        num (int): get the history by providing the index of the
        history info

    Returns:
        json: return the history information under this index.
    """
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

     Returns:
         json: return information about the result of recent
         processed images.
     """
    r = requests.get("http://127.0.0.1:5000/api/"
                     "most_recent_processed_image/{}".format(ids))
    answer = r.json()
    print(answer)
    return answer


if __name__ == '__main__':
    a = request_recent_process_images("1_a")
