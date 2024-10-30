from datetime import datetime
from functools import wraps

import pytz
from flask import jsonify
from flask_jwt_extended import jwt_required
from jwt import ExpiredSignatureError, InvalidTokenError


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return jwt_required()(fn)(*args, **kwargs)
        except (ExpiredSignatureError, InvalidTokenError):
            return jsonify({"msg": "Login session expired"}), 440

    return wrapper


def get_current_time():
    return datetime.now(pytz.timezone('Asia/Shanghai'))
