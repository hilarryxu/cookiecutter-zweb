# -*- coding: utf-8 -*-

import functools

from .errors import (
    Error, ERROR_CODE_NOT_LOGINED
)


def login_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise Error(ERROR_CODE_NOT_LOGINED)
        return method(self, *args, **kwargs)
    return wrapper
