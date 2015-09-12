# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.cache
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""

from datetime import timedelta
from functools import wraps

from .after_this_request import AfterThisRequestResponseHandler, AfterThisRequestRequestHandler, \
    AfterThisRequestCallbackRegistryProvider
from .callback import SetCacheControlHeadersCallback
from .callback import SetCacheControlHeadersFromTimedeltaCallback, SetCacheControlHeadersForNoCachingCallback


#----------------------------------------------------------------------
def cache_for(**timedelta_kw):
    """
    Set Cache-Control headers by timedelta kw
    """
    max_age_timedelta = timedelta(**timedelta_kw)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersFromTimedeltaCallback(max_age_timedelta)
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


#----------------------------------------------------------------------
def cache(*cache_control_items, **cache_control_kw):
    """
    Set Cache-Control headers by kw or item-list
    """
    cache_control_kw.update(cache_control_items)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersCallback(**cache_control_kw)
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


#----------------------------------------------------------------------
def dont_cache():
    """
    Set Cache-Control headers for no caching
    """
    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersForNoCachingCallback()
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


########################################################################
class FlaskCacheControl(object):

    #----------------------------------------------------------------------
    def __init__(self, app=None):
        self._app = app
        if app:
            self.init_app(app)

    #----------------------------------------------------------------------
    def init_app(self, app):
        self._register_request_handler(app)
        self._register_response_handler(app)

    #----------------------------------------------------------------------
    def _register_request_handler(self, app):
        app.before_request(AfterThisRequestRequestHandler())

    #----------------------------------------------------------------------
    def _register_response_handler(self, app):
        app.after_request(AfterThisRequestResponseHandler())
