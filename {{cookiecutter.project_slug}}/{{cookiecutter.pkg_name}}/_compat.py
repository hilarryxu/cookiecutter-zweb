# -*- coding: utf-8 -*-

"""Python 2/3 compatibility module."""

import sys

from tornado.util import (  # noqa
    _BASESTRING_TYPES,
    _TO_UNICODE_TYPES,
    _UTF8_TYPES,
    native_str,
    recursive_unicode,
    to_basestring,
    to_unicode,
    utf8,
)

PY3 = sys.version_info >= (3,)

if PY3:
    xrange = range

if PY3:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    integer_types = (int,)
    unicode = str
    basestring = (str, bytes)
else:
    text_type = unicode  # noqa
    binary_type = str
    string_types = (str, unicode)  # noqa
    integer_types = (int, long)  # noqa
    unicode = unicode  # noqa
    basestring = basestring  # noqa

if PY3:
    unicode_type = str
    basestring_type = str
else:
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa
