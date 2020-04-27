# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import math
import time
import uuid

from tornado.escape import json_decode, json_encode
from zweb.orm.util import safestr, safeunicode  # noqa


class Storage(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


storage = Storage


def md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def gen_cookie_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


def strftm(tm=None, fmt='%Y-%m-%d %H:%M:%S'):
    if tm is None:
        tm = int(time.time())
    tm = int(tm)
    if tm <= 100:
        return ''
    return time.strftime(fmt, time.localtime(tm))


def str2tm(s, fmt='%Y-%m-%d %H:%M:%S'):
    obj = datetime.datetime.strptime(s, fmt)
    return int(time.mktime(obj.timetuple()))


def iif(cond, yes, no=''):
    if cond:
        return yes
    return no


def get_pager(total_count, per_page, page):
    max_page = int(math.ceil(total_count / (per_page * 1.0)))
    offset = (page - 1) * per_page
    env = storage()
    env.per_page = per_page
    env.max_page = max_page
    env.page = page
    env.total_count = total_count
    env.offset = offset
    return env


def choice_values(choices):
    return [e[0] for e in choices]


def get_choice_label(choices, value, default=''):
    for v, label in choices:
        if v == value:
            return label
    return default


def as_int(v, default=0):
    if not v:
        return default
    return int(v)


def m2dict(d):
    if d:
        if hasattr(d, 'to_dict'):
            d = d.to_dict()
        ctx = storage()
        props_val = d.pop('props', None)
        if props_val:
            ctx.update(json_decode(props_val))
        ctx.update(d)
        return ctx
    else:
        return {}


def update_props(obj, new_props):
    if obj.is_new():
        setattr(obj, 'props', '')
    props = obj.props
    if not props:
        props = {}
    else:
        props = json_decode(props)
    props.update(new_props)
    obj.props = json_encode(props)


tpl_context = dict(strftm=strftm, iif=iif, get_choice_label=get_choice_label)
