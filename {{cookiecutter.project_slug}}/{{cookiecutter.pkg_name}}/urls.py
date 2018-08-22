# -*- coding: utf-8 -*-

import os

from .config import DEBUG, COOKIE_SECRET
from .views import _url  # noqa
from .views._route import route, api_route
from .views._view import NotFound, ApiNotFound

settings = dict(
    debug=DEBUG,
    cookie_secret=COOKIE_SECRET,
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_prefix='/static/',
    login_url='/login',
)

handlers = [
] + route.handlers + api_route.handlers + [
    (r'/api/.*', ApiNotFound),
    (r'.*', NotFound)
]
