# -*- coding: utf-8 -*-

handlers = {}


class RPC:
    FLAG_NO_AUTH = 'no_auth'

    def register(self, service, method, **kwargs):
        def _wrapper(handler):
            key = f'{service}.{method}'
            kwargs['_key'] = key
            kwargs['_handler'] = handler
            handlers[key] = kwargs
            return handler

        return _wrapper

    def find_handler(self, name):
        return handlers.get(name, None)


rpc = RPC()
