# -*- coding: utf-8 -*-

import os

from .config import COOKIE_SECRET, DEBUG
from .views import _url  # noqa
from .views._route import api_route, route
from .views._view import ApiNotFound, NotFound

settings = dict(
    debug=DEBUG,
    cookie_secret=COOKIE_SECRET,
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_prefix='/static/',
    login_url='/login',
)

handlers = (
    []
    + route.handlers
    + api_route.handlers
    + [(r'/api/.*', ApiNotFound), (r'.*', NotFound)]
)
