# -*- coding: utf-8 -*-


class Route(object):
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.handlers = []

    def __call__(self, url, **kwds):
        name = kwds.pop('name', None)
        if self.base_url:
            url = '/' + self.base_url.strip('/') + '/' + url.lstrip('/')

        def _(cls):
            self.handlers.append((url, cls, kwds, name))
            return cls

        return _


route = Route()
api_route = Route('api')
