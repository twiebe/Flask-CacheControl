# -*- coding: utf-8 -*-
"""
    flask_cachecontrol.error
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Thomas Wiebe.
    :license: BSD, see LICENSE for more details.
"""


class FlaskCacheControlError(Exception):
    pass


class CacheControlAttributeInvalidError(FlaskCacheControlError):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __str__(self):
        return 'Attribute {!r} not a valid Flask Cache-Control parameter'.format(
            self.attr_name)
