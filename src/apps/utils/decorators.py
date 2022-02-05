from functools import wraps
from flask import request
def json_only(function):
    @wraps(function)
    def decorator(*args,**kwargs):
        if not request.is_json:
            return {"error": "request is not json"}, 400
        return function(*args,**kwargs)
    return decorator
