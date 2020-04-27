# -*- coding: utf-8 -*-

from .core import rpc

SERVICE = 'CommonService'


@rpc.register(service=SERVICE, method='test', flags=[rpc.FLAG_NO_AUTH])
def do_test(handler, request, ctx):
    return handler.api_ok()
