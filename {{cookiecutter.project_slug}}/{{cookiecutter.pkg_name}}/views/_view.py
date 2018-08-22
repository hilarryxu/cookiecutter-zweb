# -*- coding: utf-8 -*-

import logging
from distutils.util import strtobool
import traceback
import time
import json

from tornado import web
from tornado import escape
from tornado.escape import json_decode

from .. import config as g
from .. import consts
from ..utils import safestr, tpl_context
from .. import helpers
from ..errors import (
    Error, ERROR_CODE_SYSTEM,
    ERROR_CODE_PARAM_WRONG
)
from ..models import User


class BaseView(web.RequestHandler):
    def get_argument(self, name, default=web.RequestHandler._ARG_DEFAULT, strip=True, type=None):
        arg = super(BaseView, self).get_argument(name, default, strip)
        if type is not None:
            try:
                if type is bool:
                    arg = strtobool(str(arg))
                else:
                    arg = type(arg)
            except (ValueError, TypeError):
                if arg is None and default is None:
                    return arg
                raise web.MissingArgumentError(
                    "Invalid argument '%s' of type '%s' for %s" % (arg, type.__name__, name))
        return arg

    def api_error(self, arg1=None, **kwargs):
        out = {
            'code': 1
        }
        out.update(kwargs)
        out.update({
            'msg': arg1 or ''
        })
        logger = logging.getLogger('request')
        logger.warn(json.dumps(out))
        self.finish(out)

    def api_ok(self, arg1=None, **kwargs):
        out = {
            'code': 0
        }
        out.update(kwargs)
        out.update({
            'msg': arg1 or ''
        })
        self.finish(out)

    def page_limit(self):
        page = self.get_argument('page', default=1, type=int)
        limit = self.get_argument('limit', default=g.DEFAULT_LIMIT, type=int)
        return page, limit


class View(BaseView):
    def render(self, template_name=None, **kwds):
        if not self._finished:
            kwds['g'] = g
            kwds['consts'] = consts
            kwds['helpers'] = helpers
            kwds['handler'] = self
            kwds['request'] = self.request
            kwds['reverse_url'] = self.reverse_url
            kwds['static_url'] = self.static_url
            kwds['current_user'] = self.current_user
            kwds['_'] = self.locale.translate
            kwds['escape'] = escape
            kwds.update(tpl_context)
            self.finish(g.st(template_name, **kwds))

    def get_current_user(self):
        uid = self.get_secure_cookie(g.AUTH_COOKIE_KEY)
        if uid:
            p_user = User.objects.get(uid)
            return p_user

    @property
    def current_user_id(self):
        if self.current_user:
            return self.current_user.id

    def get_context(self):
        context = dict(
            base_template=getattr(self, 'base_template', '/{}/base.mako'.format(g.PKG_NAME)),
            active_domain=getattr(self, 'active_domain', ''),
            active_tab=getattr(self, 'active_tab', ''),
            js_page=getattr(self, 'js_page', ''),
            js_version=safestr(int(time.time())) if g.DEBUG else g.BUILD_VERSION
        )
        return context

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', '') == 'XMLHttpRequest'

    def write_error(self, status_code, **kwargs):
        context = self.get_context()

        error = None
        err_msg = 'ERROR %d' % int(status_code)
        if 'exc_info' in kwargs:
            exc_info = kwargs['exc_info']
            error = exc_info[1]

            if isinstance(error, web.HTTPError):
                if error.log_message:
                    err_msg = error.log_message

        if self.is_ajax():
            self.finish({
                'code': 1,
                'msg': err_msg
            })
            return

        if status_code in (404, 403):
            context['message'] = err_msg
            self.render('/{}/error/404.mako'.format(g.PKG_NAME), **context)
        elif status_code == 500:
            error_trace = ""
            if 'exc_info' in kwargs:
                for line in traceback.format_exception(*kwargs['exc_info']):
                    error_trace += line

            context.update(dict(
                debug=g.DEBUG,
                status_code=status_code,
                error_trace=error_trace
            ))
            self.render('/{}/error/500.mako'.format(g.PKG_NAME), **context)
        else:
            self.set_header('Content-Type', 'text/plain')
            self.write(err_msg)


class NotFound(View):
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class ApiView(BaseView):
    def prepare(self):
        super(ApiView, self).prepare()
        self.json_args = {}
        if self.request.headers.get('Content-Type', '').startswith('application/json'):
            try:
                self.json_args = json_decode(self.request.body)
            except Exception:
                self.json_args = {}

    def get_current_user(self):
        uid = self.get_secure_cookie(g.API_COOKIE_KEY)
        if uid:
            p_user = User.objects.get(uid)
            return p_user

    @property
    def current_user_id(self):
        if self.current_user:
            return self.current_user.id

    def set_default_headers(self):
        self.set_header('Server', 'TORNADO')

    def on_finish(self):
        logger = logging.getLogger('request')
        ctx = {
            'time_served': self.request.request_time(),
            'http_user_agent': self.request.headers.get('User-Agent', ''),
            'remote_ip': self.request.remote_ip,
            'method': self.request.method,
            'path': self.request.path,
            'arguments': self.request.arguments,
            'json_args': self.json_args,
            'current_user_id': self.current_user_id,
        }
        log_method = logger.info
        log_method(json.dumps(ctx))

    def log_exception(self, typ, value, tb):
        if isinstance(value, (Error,)):
            pass
        else:
            super(ApiView, self).log_exception(typ, value, tb)

    def write_error(self, status_code, **kwargs):
        try:
            exc_info = kwargs.pop('exc_info')
            error = exc_info[1]
            exception = ''.join([ln for ln in traceback.format_exception(*exc_info)])

            if isinstance(error, Error):
                pass
            elif isinstance(error, web.MissingArgumentError):
                error = Error(ERROR_CODE_PARAM_WRONG, error.log_message if g.DEBUG else None)
            else:
                error = Error(ERROR_CODE_SYSTEM, exception if g.DEBUG else None)

            logger = logging.getLogger('request')
            logger.warn('Error(%s)', error)

            self.set_status(200)
            self.finish({
                'code': error.code,
                'msg': error.message
            })
        except Exception:
            logging.error(traceback.format_exc())
            return super(ApiView, self).write_error(status_code, **kwargs)


class ApiNotFound(ApiView):
    def get(self):
        self.api_error('ERROR 404')

    def post(self):
        self.api_error('ERROR 404')
