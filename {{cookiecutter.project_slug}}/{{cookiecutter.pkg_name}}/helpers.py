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


def mysql_iter(model_cls, arg_id=0, limit=500, fields='*',
               filter_args=None, filter_kwargs=None):
    while True:
        if filter_args:
            qs = model_cls.objects.filter(*filter_args)
        else:
            qs = model_cls.objects.filter()
        if filter_kwargs:
            qs.filter(**filter_kwargs)

        qs.filter('id > %s', arg_id).order_by('id')
        objs = qs.column(fields, limit=limit)
        if objs:
            for obj in objs:
                yield obj
            arg_id = objs[-1].id
        else:
            break
