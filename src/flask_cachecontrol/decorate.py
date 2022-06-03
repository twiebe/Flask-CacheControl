# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.cache
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""
from datetime import timedelta
from functools import wraps

import flask

from .callback import SetCacheControlHeadersCallback, SetVaryHeaderCallback
from .callback import SetCacheControlHeadersFromTimedeltaCallback, SetCacheControlHeadersForNoCachingCallback
from .evaluator import ResponseIsSuccessful


def cache_for(only_if=ResponseIsSuccessful, vary=None, **timedelta_kw):
    """
    Set Cache-Control headers and Expires-header.

    Takes timedelta instantiation kw args.

    By default, only applies to successful requests (2xx status code).
    Provide only_if=Always to apply to all requests or supply custom
    evaluator for customized behaviour.

    Optionally takes vary as list of headers. If given. Vary-header is
    returned for all requests - successful or failed.
    """
    max_age_timedelta = timedelta(**timedelta_kw)
    cache_callback = only_if(SetCacheControlHeadersFromTimedeltaCallback(max_age_timedelta))
    vary_callback = SetVaryHeaderCallback(vary)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            flask.after_this_request(cache_callback)
            flask.after_this_request(vary_callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


def cache(*cache_control_items, only_if=ResponseIsSuccessful, vary=None, **cache_control_kw):
    """
    Set Cache-Control headers.

    Expects keyword arguments and/or an item list.

    Each pair is used to set Flask Response.cache_control attributes,
    where the key is the attribute name and the value is its value.

    Use True as value for attributes without values.

    In case of an invalid attribute, CacheControlAttributeInvalidError
    will be thrown.

    By default, only applies to successful requests (2xx status code).
    Provide only_if=Always to apply to all requests or supply custom
    evaluator for customized behaviour.

    Optionally takes vary as list of headers. If given. Vary-header is
    returned for all requests - successful or failed.
    """
    cache_control_kw.update(cache_control_items)
    cache_callback = only_if(SetCacheControlHeadersCallback(**cache_control_kw))
    vary_callback = SetVaryHeaderCallback(vary)

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            flask.after_this_request(cache_callback)
            flask.after_this_request(vary_callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func


def dont_cache(only_if=ResponseIsSuccessful):
    """
    Set Cache-Control headers for no caching

    Will generate proxy-revalidate, no-cache, no-store, must-revalidate,
    max-age=0.

    By default, only applies to successful requests (2xx status code).
    Provide only_if=Always to apply to all requests or supply custom
    evaluator for customized behaviour.
    """
    cache_callback = only_if(SetCacheControlHeadersForNoCachingCallback())

    def decorate_func(func):
        @wraps(func)
        def decorate_func_call(*a, **kw):
            flask.after_this_request(cache_callback)
            return func(*a, **kw)
        return decorate_func_call
    return decorate_func
