# Flask-CacheControl

## Description:

A light-weight library to conveniently set Cache-Control
headers on the response. Decorate view functions with
cache_for, cache, or dont_cache decorators. Makes use of
Flask response.cache_control.

This extension does not provide any caching of its own. Its sole
purpose is to set Cache-Control and related HTTP headers on the
response, so that clients, intermediary proxies or reverse proxies
in your jurisdiction which evaluate Cache-Control headers, such as
Varnish Cache, do the caching for you.

## Example:
```python
from flask.ext.cachecontrol import (
    FlaskCacheControl,
    cache,
    cache_for,
    dont_cache)
flask_cache_control = FlaskCacheControl()
flask_cache_control.init_app(app)

@cache_for(hours=3)
def index_view():
    return render_template('index_template')

@cache(max_age=3600, public=True)
def stats_view():
    return render_template('stats_template')

@dont_cache()
def dashboard_view():
    return render_template('dashboard_template')
```
