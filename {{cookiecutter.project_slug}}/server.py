#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from pprint import pformat

ROOT = os.path.abspath(os.path.dirname(__file__))  # noqa
sys.path.append(os.path.join(ROOT, '.site-packages'))  # noqa

from {{cookiecutter.pkg_name}} import config as C  # noqa
from {{cookiecutter.pkg_name}}.db import setup_model
setup_model(C.DEBUG)  # noqa
from {{cookiecutter.pkg_name}}.config import DEBUG, ADDRESS, PORT, XHEADERS
from {{cookiecutter.pkg_name}}.app import make_app
from {{cookiecutter.pkg_name}}.urls import settings


def main():
    import tornado.ioloop
    from tornado.options import options, define

    define('port', default=PORT, type=int, help='run server on this port')
    if DEBUG:
        options.logging = 'debug'
    options.parse_command_line()

    app = make_app(ROOT, **settings)
    loop = tornado.ioloop.IOLoop.current()
    app.listen(options.port, ADDRESS, xheaders=XHEADERS)

    msg = 'Listening on %s:%s' % (ADDRESS, options.port)
    logging.info(msg)
    logging.debug("Settings: %s", pformat(settings))

    loop.start()


if __name__ == '__main__':
    main()
