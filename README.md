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
from flask_cachecontrol import (
    FlaskCacheControl,
    cache,
    cache_for,
    dont_cache)
flask_cache_control = FlaskCacheControl()
flask_cache_control.init_app(app)

@app.route('/')
@cache_for(hours=3)
def index_view():
    return render_template('index_template')

@app.route('/stats')
@cache(max_age=3600, public=True)
def stats_view():
    return render_template('stats_template')

@app.route('/dashboard')
@dont_cache()
def dashboard_view():
    return render_template('dashboard_template')
```

## Breaking Changes:

### v0.2.0
- By default, cache control headers are only applied to successful requests. (status code `2xx`) This behaviour can be customized by providing `only_if=` as a kw to all caching decorators.
- Requires python 3.3 or higher
