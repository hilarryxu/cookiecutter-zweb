# -*- coding: utf-8 -*-

from tornado.escape import json_decode

from ._route import api_route
from ._view import ApiView
from ..db import _rdb
from ..consts import (
    KEY_CONFIG
)


@api_route('/config')
class ConfigView(ApiView):
    def get(self):
        config = {}
        val = _rdb.get(KEY_CONFIG)
        if val:
            config = json_decode(val)

        return self.api_ok(data=config)
