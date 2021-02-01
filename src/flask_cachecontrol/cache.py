# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.cache
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""
from abc import ABCMeta, abstractmethod
from datetime import timedelta
from functools import wraps

from .after_this_request import AfterThisRequestResponseHandler, AfterThisRequestRequestHandler, \
    AfterThisRequestCallbackRegistryProvider
from .callback import SetCacheControlHeadersCallback
from .callback import SetCacheControlHeadersFromTimedeltaCallback, SetCacheControlHeadersForNoCachingCallback


class OnlyIfEvaluatorBase(metaclass=ABCMeta):
    def __init__(self, callback):
        self._callback = callback

    def __call__(self, response):
        if self._response_qualifies(response):
            self._callback(response)

    @abstractmethod
    def _response_qualifies(self, response):
        pass


class Always(OnlyIfEvaluatorBase):
    def _response_qualifies(self, response):
        return True


class ResponseIsSuccessful(OnlyIfEvaluatorBase):
    def _response_qualifies(self, response):
        return 200 <= response.status_code < 300


def cache_for(only_if=ResponseIsSuccessful, **timedelta_kw):
    """
    Set Cache-Control headers and Expires-header.

    Expects a timedelta instance.

    By default only applies to successful requests (2xx status code).
    Provide only_if=None to apply to all requests or supply custom
    evaluator for customized behaviour.
    """
    max_age_timedelta = timedelta(**timedelta_kw)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersFromTimedeltaCallback(max_age_timedelta)
            if only_if is not None:
                callback = only_if(callback)
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


def cache(*cache_control_items, only_if=ResponseIsSuccessful, **cache_control_kw):
    """
    Set Cache-Control headers.

    Expects keyword arguments and/or an item list.

    Each pair is used to set Flask Response.cache_control attributes,
    where the key is the attribute name and the value is its value.

    Use True as value for attributes without values.

    In case of an invalid attribute, CacheControlAttributeInvalidError
    will be thrown.

    By default only applies to successful requests (2xx status code).
    Provide only_if=None to apply to all requests or supply custom
    evaluator for customized behaviour.
    """
    cache_control_kw.update(cache_control_items)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersCallback(**cache_control_kw)
            if only_if is not None:
                callback = only_if(callback)
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


def dont_cache(only_if=ResponseIsSuccessful):
    """
    Set Cache-Control headers for no caching

    Will generate proxy-revalidate, no-cache, no-store, must-revalidate,
    max-age=0.

    By default only applies to successful requests (2xx status code).
    Provide only_if=None to apply to all requests or supply custom
    evaluator for customized behaviour.
    """
    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            callback = SetCacheControlHeadersForNoCachingCallback()
            if only_if is not None:
                callback = only_if(callback)
            registry_provider = AfterThisRequestCallbackRegistryProvider()
            registry = registry_provider.provide()
            registry.add(callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


class FlaskCacheControl:
    def __init__(self, app=None):
        self._app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self._register_request_handler(app)
        self._register_response_handler(app)

    def _register_request_handler(self, app):
        app.before_request(AfterThisRequestRequestHandler())

    def _register_response_handler(self, app):
        app.after_request(AfterThisRequestResponseHandler())
