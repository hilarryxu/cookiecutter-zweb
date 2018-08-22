# -*- coding: utf-8 -*-

import os

from mako.lookup import TemplateLookup

DEBUG = True
ADDRESS = ''
PORT = 3000
XHEADERS = False

PKG_NAME = '{{cookiecutter.pkg_name}}'
BUILD_VERSION = 'v0'
DEFAULT_LIMIT = 10
API_COOKIE_KEY = '{}_user'.format(PKG_NAME)
AUTH_COOKIE_KEY = '{}_user'.format(PKG_NAME)

ROOT = os.path.abspath(os.path.dirname(__file__))
RENDER_PATH = [
    os.path.join(ROOT, 'templates')
]

UPLOAD_PATH_PREFIX = os.path.join(ROOT, 'static/upload')
UPLOAD_URL_PREFIX = '/static/upload'

try:
    from .local_config import *  # noqa
except ImportError:
    pass

module_directory = '/tmp/%s' % RENDER_PATH[0].strip('/').replace('/', '.')

template_lookup = TemplateLookup(
    directories=tuple(RENDER_PATH),
    module_directory=module_directory,
    encoding_errors='ignore',
    imports=['from %s.utils import safeunicode' % PKG_NAME],
    default_filters=['safeunicode', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8'
)


def st(html, **kwds):
    tpl = template_lookup.get_template(html)
    return tpl.render(**kwds)
