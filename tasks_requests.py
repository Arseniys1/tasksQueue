import jsonpickle
import requests
from __init__ import __fullname__


def request(url, data):
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Server": __fullname__
    }
    requests.post(url, jsonpickle.encode(data, unpicklable=False), headers=headers)


def success_request(url, task):
    request(url, create_request_data(True, task))


def error_request(url, task):
    request(url, create_request_data(False, task))


def create_request_data(success, task):
    return {
        "success": success,
        "task": task,
        "callback_success_url": task.task_data.get_callback_success_url(),
        "callback_error_url": task.task_data.get_callback_error_url(),
    }

