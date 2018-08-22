# -*- coding: utf-8 -*-

import hashlib
import hmac

from tornado.web import HTTPError

from .config import PASSWORD_SECRET
from .utils import safestr


def get_object_or_404(model_cls, **kwargs):
    obj = model_cls.objects.get(**kwargs)
    if not obj:
        raise HTTPError(404, '资源未找到')
    return obj


def make_password(s):
    s = safestr(s)
    val = hmac.new(PASSWORD_SECRET, s, hashlib.sha1).hexdigest()
    return safestr(val)
