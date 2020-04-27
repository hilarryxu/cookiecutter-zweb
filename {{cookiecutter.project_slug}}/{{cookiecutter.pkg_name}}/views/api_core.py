# -*- coding: utf-8 -*-

from tornado.escape import json_decode

from ..consts import KEY_CONFIG
from ..db import _rdb
from ._route import api_route
from ._view import ApiView


@api_route('/config')
class ConfigView(ApiView):
    def get(self):
        config = {}
        val = _rdb.get(KEY_CONFIG)
        if val:
            config = json_decode(val)

        return self.api_ok(data=config)
