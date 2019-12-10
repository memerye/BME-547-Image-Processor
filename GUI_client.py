import requests


def validate_user(x):
    r = requests.post("##", json=x)
    answer = r.json()
    return answer
