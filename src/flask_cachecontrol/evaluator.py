# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.evaluator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""
from abc import ABCMeta, abstractmethod


class OnlyIfEvaluatorBase(metaclass=ABCMeta):
    def __init__(self, callback):
        self._callback = callback

    def __call__(self, response):
        if self._response_qualifies(response):
            return self._callback(response)
        return response

    @abstractmethod
    def _response_qualifies(self, response):
        pass


class Always(OnlyIfEvaluatorBase):
    """
    Matches all responses.
    """
    def _response_qualifies(self, response):
        return True


class ResponseIsSuccessful(OnlyIfEvaluatorBase):
    """
    Matches responses with a 2xx status code
    """
    def _response_qualifies(self, response):
        return 200 <= response.status_code < 300


class ResponseIsSuccessfulOrRedirect(OnlyIfEvaluatorBase):
    """
    Matches responses with 2xx and 3xx status codes.
    """
    def _response_qualifies(self, response):
        return 200 <= response.status_code < 400
