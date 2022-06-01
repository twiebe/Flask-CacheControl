import pytest
from flask import Flask, Response
from flask_cachecontrol import FlaskCacheControl, cache_for, cache, dont_cache, ResponseIsSuccessful, Always
from flask_cachecontrol.cache import ResponseIsSuccessfulOrRedirect

app = Flask(__name__)

flask_cache_control = FlaskCacheControl(app)


@app.route('/cache_for/on_success/<int:status_code>')
@cache_for(only_if=ResponseIsSuccessful, seconds=300)
def view_cache_for_on_success(status_code):
    return Response(status=status_code)


@app.route('/cache_for/on_success_or_redirect/<int:status_code>')
@cache_for(only_if=ResponseIsSuccessfulOrRedirect, seconds=300)
def view_cache_for_on_success_or_redirect(status_code):
    return Response(status=status_code)


@app.route('/cache_for/always/<int:status_code>')
@cache_for(only_if=Always, seconds=300)
def view_cache_for_always(status_code):
    return Response(status=status_code)


@app.route('/dont_cache/always/<int:status_code>')
@dont_cache(only_if=Always)
def view_dont_cache_always(status_code):
    return Response(status=status_code)


@app.route('/dont_cache/on_success/<int:status_code>')
@dont_cache(only_if=ResponseIsSuccessful)
def view_dont_cache_on_success(status_code):
    return Response(status=status_code)


@app.route('/dont_cache/on_success_or_redirect/<int:status_code>')
@dont_cache(only_if=ResponseIsSuccessfulOrRedirect)
def view_dont_cache_on_success_or_redirect(status_code):
    return Response(status=status_code)


@app.route('/cache/always/<int:status_code>')
@cache(no_store=True, only_if=Always)
def view_cache_always(status_code):
    return Response(status=status_code)


@app.route('/cache/on_success/<int:status_code>')
@cache(no_store=True, only_if=ResponseIsSuccessful)
def view_cache_on_success(status_code):
    return Response(status=status_code)


@app.route('/cache/on_success_or_redirect/<int:status_code>')
@cache(no_store=True, only_if=ResponseIsSuccessfulOrRedirect)
def view_cache_on_success_or_redirect(status_code):
    return Response(status=status_code)


@app.route('/cache/always_only_if_none/<int:status_code>')
@cache(no_store=True, only_if=None)
def view_cache_on_success_only_if_none(status_code):
    return Response(status=status_code)


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


class TestCacheForAlways:
    def test_success(self, client):
        rv = client.get('/cache_for/always/200')
        assert 'Cache-Control' in rv.headers and rv.headers['Cache-Control'] == 'max-age=300'
        assert 'Expires' in rv.headers

    def test_failure(self, client):
        rv = client.get('/cache_for/always/404')
        assert 'Cache-Control' in rv.headers and rv.headers['Cache-Control'] == 'max-age=300'
        assert 'Expires' in rv.headers


class TestCacheForOnlyOnSuccess:
    def test_success(self, client):
        rv = client.get('/cache_for/on_success/200')
        assert 'Cache-Control' in rv.headers

    def test_redirect(self, client):
        rv = client.get('/cache_for/on_success/300')
        assert 'Cache-Control' not in rv.headers

    def test_failure(self, client):
        rv = client.get('/cache_for/on_success/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheForOnlyOnSuccessOrRedirect:
    def test_success(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/200')
        assert 'Cache-Control' in rv.headers

    def test_redirect(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/300')
        assert 'Cache-Control' in rv.headers

    def test_failure(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/404')
        assert 'Cache-Control' not in rv.headers


class TestDontCacheAlways:
    def test_success(self, client):
        rv = client.get('/dont_cache/always/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/always/300')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_failure(self, client):
        rv = client.get('/dont_cache/always/404')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']


class TestDontCacheOnlyOnSuccess:
    def test_success(self, client):
        rv = client.get('/dont_cache/on_success/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/on_success/300')
        assert 'Cache-Control' not in rv.headers

    def test_failure(self, client):
        rv = client.get('/dont_cache/on_success/404')
        assert 'Cache-Control' not in rv.headers


class TestDontCacheOnlyOnSuccessOrRedirect:
    def test_success(self, client):
        rv = client.get('/dont_cache/on_success_or_redirect/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/on_success_or_redirect/300')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_failure(self, client):
        rv = client.get('/dont_cache/on_success_or_redirect/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheAlways:
    def test_success(self, client):
        rv = client.get('/cache/always/200')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/cache/always/300')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_failure(self, client):
        rv = client.get('/cache/always/404')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']


class TestCacheOnlyOnSuccess:
    def test_success(self, client):
        rv = client.get('/cache/on_success/200')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/cache/on_success/300')
        assert 'Cache-Control' not in rv.headers

    def test_failure(self, client):
        rv = client.get('/cache/on_success/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheOnlyOnSuccessOrRedirect:
    def test_success(self, client):
        rv = client.get('/cache/on_success_or_redirect/200')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/cache/on_success_or_redirect/300')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_failure(self, client):
        rv = client.get('/cache/on_success_or_redirect/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheAlwaysOnlyIfNone:
    def test_success(self, client):
        rv = client.get('/cache/always_only_if_none/200')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/cache/always_only_if_none/300')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']

    def test_failure(self, client):
        rv = client.get('/cache/always_only_if_none/404')
        assert 'Cache-Control' in rv.headers \
               and 'no-store' in rv.headers['Cache-Control'] \
               and 'no-cache' not in rv.headers['Cache-Control']
