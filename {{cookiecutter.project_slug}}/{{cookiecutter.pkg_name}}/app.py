# -*- coding: utf-8 -*-

import os.path

import tornado.locale
import tornado.web

from .config import PKG_NAME
from .urls import handlers


class Application(tornado.web.Application):
    def __init__(self, **kwargs):
        kwargs.update(handlers=handlers)
        super(Application, self).__init__(**kwargs)


def make_app(project_root, **kwargs):
    locale_path = os.path.join(project_root, PKG_NAME + '/locale')
    if os.path.exists(locale_path):
        tornado.locale.load_translations(locale_path)
    app = Application(**kwargs)
    return app
