from functools import wraps
import json
from helper.utils import *


def fetch_data(filtered_func):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                filter_by = kwargs["filter_by"]
                file = kwargs["file"]
                data = kwargs.get("data", [])

                filtered = eval(filtered_func + kwargs["type"])

                with open(file, "r", encoding="utf-8") as file:
                    json_data = json.load(file)
                    if filter_by is not None:
                        data = filtered(json_data, filter_by)
                    else:
                        data = json_data
                kwargs["data"] = data
                return func(*args, **kwargs)
            except Exception as e:
                raise Exception(*e.args)

        return wrapper

    return decorate
