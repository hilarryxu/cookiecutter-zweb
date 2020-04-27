# -*- coding: utf-8 -*-

from ..errors import ERROR_CODE_NOT_LOGINED, Error
from ..views._route import api_route
from ..views._view import RPCView
from .core import handlers, rpc


def format_ctx(ctx):
    out = {}
    for k, v in ctx.items():
        if k == '_key':
            continue
        elif k == '_handler':
            out[k] = v.__name__
        else:
            out[k] = v
    return out


@api_route(r'/rpc/(.*)', name='rpc')
class RPCFacadeView(RPCView):
    def get(self, url_path):
        return self.run_rpc(url_path)

    def post(self, url_path):
        return self.run_rpc(url_path)

    def run_rpc(self, url_path):
        inspect = self.get_argument('_inspect', '')
        if inspect:
            data = {
                'url_path': url_path,
                'handlers': {k: format_ctx(v) for k, v in handlers.items()},
            }
            return self.api_ok(data=data)

        url_parts = url_path.rstrip('/').split('/')
        rpc_handler_name = url_parts[0]

        ctx = rpc.find_handler(rpc_handler_name)
        if not ctx:
            return self.api_error('no such handler')

        rpc_handler = ctx['_handler']
        flags = ctx.get('flags', [])
        if rpc.FLAG_NO_AUTH not in flags:
            if not self.current_user:
                raise Error(ERROR_CODE_NOT_LOGINED)
        return rpc_handler(self, self.request, ctx)
