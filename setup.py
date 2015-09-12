"""
Flask-CacheControl
------------------

A light-weight library to conveniently set Cache-Control
headers on the response. Decorate view functions with
cache_for, cache, or dont_cache decorators. Makes use of
Flask response.cache_control.

This extension does not provide any caching of its own. Its sole
purpose is to set Cache-Control and related HTTP headers on the
response, so that clients, intermediary proxies or reverse proxies
in your jurisdiction which evaluate Cache-Control headers, such as
Varnish Cache, do the caching for you.
"""

import ast
import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/flask_cachecontrol/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='Flask-CacheControl',
    version=version,
    url='https://github.com/twiebe/Flask-CacheControl',
    license='BSD',
    author='Thomas Wiebe',
    author_email='code@heimblick.net',
    description='Set Cache-Control headers on the Flask response',
    long_description=__doc__,
    package_dir={'': 'src'},
    packages=['flask_cachecontrol'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)