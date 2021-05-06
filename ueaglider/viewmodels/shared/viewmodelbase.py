from typing import Optional
import datetime
import uuid
import flask
from flask import Request

from ueaglider.infrastructure import request_dict, cookie_auth


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')
        self.year = datetime.datetime.now().year
        self.nonce = uuid.uuid4().hex
        self.error: Optional[str] = None
        self.message: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)

    def to_dict(self):
        return self.__dict__
