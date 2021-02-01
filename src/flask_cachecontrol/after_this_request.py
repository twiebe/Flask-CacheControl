# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.after_this_request
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""
from abc import ABCMeta, abstractmethod

from flask import g


class CallbackBase(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, response):
        pass


class CallbackRegistry:
    def __init__(self):
        self._callbacks = []

    def add(self, callback):
        self._callbacks.append(callback)

    def __iter__(self):
        while self._callbacks:
            yield self._callbacks.pop(0)


class AfterThisRequestCallbackRegistryProvider:
    def provide(self):
        return g.after_this_request_callback_registry


class AfterThisRequestResponseProcessor:
    def __init__(self, response):
        self._response = response
        self._callback_registry = None
        self._callback = None

    def process(self):
        self._fetch_callback_registry()
        for self._callback in self._callback_registry:
            self._execute_callback()

    def _fetch_callback_registry(self):
        provider = AfterThisRequestCallbackRegistryProvider()
        self._callback_registry = provider.provide()

    def _execute_callback(self):
        self._callback(self._response)


class AfterThisRequestResponseHandler:
    def __call__(self, response):
        self._process_response(response)
        return response

    def _process_response(self, response):
        processor = AfterThisRequestResponseProcessor(response)
        processor.process()


class AfterThisRequestRequestHandler:
    def __call__(self):
        if not self._callback_registry_set_up_on_g():
            self._setup_callback_registry_on_g()

    def _callback_registry_set_up_on_g(self):
        return getattr(g, 'after_this_request_callback_registry', None) is not None

    def _setup_callback_registry_on_g(self):
        g.after_this_request_callback_registry = CallbackRegistry()
