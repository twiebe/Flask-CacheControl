# Flask-CacheControl

## Description

A light-weight library to conveniently set `Cache-Control`
headers on the response. Decorate view functions with
`cache_for`, `cache`, or `dont_cache` decorators. Makes use of
Flask `response.cache_control`.

This extension does not provide any caching of its own. Its sole
purpose is to set `Cache-Control` and related HTTP headers on the
response, so that clients, intermediary proxies or reverse proxies
in your jurisdiction which evaluate `Cache-Control` headers, such as
Varnish Cache, do the caching for you.

By default, `Cache-Control` headers are only appended in case of a
successful response (status code 2xx). This behaviour can be controlled
with the `only_if` argument to `cache_for` and `cache` decorators. Included
options are `Always`, `ResponseIsSuccessful`, `ResponseIsSuccessfulOrRedirect`. Custom behaviour can be implemented by subclassing `OnlyIfEvaluatorBase`.

If the `vary` keyword argument is given to `cache_for` or `cache` 
decorators, the `Vary` HTTP header is returned with the response.
`Vary` headers are appended independent of response status code.

## Example
```python
from flask import Flask, render_template
from flask_cachecontrol import (
    cache,
    cache_for,
    dont_cache,
    Always, 
    ResponseIsSuccessfulOrRedirect)


app = Flask(__name__)


@app.route('/')
@cache_for(hours=3)
def index_view():
    return render_template('index_template')

@app.route('/users')
@cache_for(minutes=5, only_if=ResponseIsSuccessfulOrRedirect)
def users_view():
    return render_template('user_template')

@app.route('/stats')
@cache(max_age=3600, public=True, only_if=Always, vary=['User-Agent', 'Referer'])
def stats_view():
    return render_template('stats_template')

@app.route('/dashboard')
@dont_cache()
def dashboard_view():
    return render_template('dashboard_template')
```

## Changelog
### 0.3.0
- Add `only_if` evaluator for _successful or redirect (2xx, 3xx)_ responses (#7)
- Support **Vary**-headers (#6)
- Improve instantiation of callbacks and registry provider
- **BREAKING**: Simplify instantiation and hooking into flask response handling (#8)
  - No more need to instantiate `FlaskCacheControl` for Flask app.
- **BREAKING**: Drop support for `only_if=None`
  - Use more explicit `only_if=Always` instead
- **BREAKING**: Restructure modules
  - Direct imports from modules inside the package need to be adapted.
- Improve test structuring
- Fix flask instantiation and import in example

### v0.2.1
- Fix import statement in example

### v0.2.0
- Add tests
- **BREAKING**: By default, cache control headers are only applied to successful requests. (status code `2xx`) This behaviour can be customized by providing `only_if=` as a kw to all caching decorators.
- **BREAKING**: Requires python 3.3 or higher
