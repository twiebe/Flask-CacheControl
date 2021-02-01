# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.callback
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime

from .after_this_request import CallbackBase
from .error import CacheControlAttributeInvalidError


class SetCacheControlHeadersFromTimedeltaCallback(CallbackBase):
    def __init__(self, timedelta):
        self._timedelta = timedelta

    def __call__(self, response):
        response.expires = datetime.utcnow() + self._timedelta
        response.cache_control.max_age = int(self._timedelta.total_seconds())


class SetCacheControlHeadersCallback(CallbackBase):
    def __init__(self, **cache_control_kw):
        self._cache_control_kw = cache_control_kw

    def __call__(self, response):
        cache_control = response.cache_control
        for attr_name, value in self._cache_control_kw.items():
            if not hasattr(cache_control, attr_name):
                raise CacheControlAttributeInvalidError(attr_name)
            setattr(cache_control, attr_name, value)


class SetCacheControlHeadersForNoCachingCallback(CallbackBase):
    def __call__(self, response):
        response.cache_control.max_age = 0
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.proxy_revalidate = True
