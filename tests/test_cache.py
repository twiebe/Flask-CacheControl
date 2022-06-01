import pytest
from flask import Flask, Response
from flask_cachecontrol import cache_for, cache, dont_cache, ResponseIsSuccessful, ResponseIsSuccessfulOrRedirect, \
    Always

app = Flask(__name__)

CACHE_SECONDS = 300
VARY_HEADERS = ['User-Agent', 'Referer']
VARY_HEADERS_STR = ','.join(VARY_HEADERS)


@app.route('/cache_for/on_success/<int:status_code>')
@cache_for(only_if=ResponseIsSuccessful, seconds=CACHE_SECONDS)
def view_cache_for_on_success(status_code):
    return Response(status=status_code)


@app.route('/cache_for/on_success_or_redirect/<int:status_code>')
@cache_for(only_if=ResponseIsSuccessfulOrRedirect, seconds=CACHE_SECONDS)
def view_cache_for_on_success_or_redirect(status_code):
    return Response(status=status_code)


@app.route('/cache_for/always/<int:status_code>')
@cache_for(only_if=Always, seconds=CACHE_SECONDS)
def view_cache_for_always(status_code):
    return Response(status=status_code)


@app.route('/cache_for/vary/<int:status_code>')
@cache_for(only_if=ResponseIsSuccessful, seconds=CACHE_SECONDS, vary=VARY_HEADERS)
def view_cache_for_on_success_with_vary(status_code):
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


@app.route('/cache/vary/<int:status_code>')
@cache(no_store=True, only_if=ResponseIsSuccessful, vary=VARY_HEADERS)
def view_cache_on_success_with_vary(status_code):
    return Response(status=status_code)


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


class TestCacheForAlways:
    def test_success(self, client):
        rv = client.get('/cache_for/always/200')
        assert 'Cache-Control' in rv.headers and rv.headers['Cache-Control'] == f'max-age={CACHE_SECONDS}'
        assert 'Expires' in rv.headers

    def test_client_error(self, client):
        rv = client.get('/cache_for/always/404')
        assert 'Cache-Control' in rv.headers and rv.headers['Cache-Control'] == f'max-age={CACHE_SECONDS}'
        assert 'Expires' in rv.headers


class TestCacheForOnlyOnSuccess:
    def test_success(self, client):
        rv = client.get('/cache_for/on_success/200')
        assert 'Cache-Control' in rv.headers

    def test_redirect(self, client):
        rv = client.get('/cache_for/on_success/300')
        assert 'Cache-Control' not in rv.headers

    def test_client_error(self, client):
        rv = client.get('/cache_for/on_success/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheForOnlyOnSuccessOrRedirect:
    def test_success(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/200')
        assert 'Cache-Control' in rv.headers

    def test_redirect(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/300')
        assert 'Cache-Control' in rv.headers

    def test_client_error(self, client):
        rv = client.get('/cache_for/on_success_or_redirect/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheForVary:
    def test_success_wo_vary(self, client):
        rv = client.get('/cache_for/on_success/200')
        assert 'Vary' not in rv.headers

    def test_success(self, client):
        rv = client.get('/cache_for/vary/200')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_redirect(self, client):
        rv = client.get('/cache_for/vary/300')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_client_error(self, client):
        rv = client.get('/cache_for/vary/404')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_server_error(self, client):
        rv = client.get('/cache_for/vary/500')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR


class TestDontCacheAlways:
    def test_success(self, client):
        rv = client.get('/dont_cache/always/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/always/300')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_client_error(self, client):
        rv = client.get('/dont_cache/always/404')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']


class TestDontCacheOnlyOnSuccess:
    def test_success(self, client):
        rv = client.get('/dont_cache/on_success/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/on_success/300')
        assert 'Cache-Control' not in rv.headers

    def test_client_error(self, client):
        rv = client.get('/dont_cache/on_success/404')
        assert 'Cache-Control' not in rv.headers


class TestDontCacheOnlyOnSuccessOrRedirect:
    def test_success(self, client):
        rv = client.get('/dont_cache/on_success_or_redirect/200')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_redirect(self, client):
        rv = client.get('/dont_cache/on_success_or_redirect/300')
        assert 'Cache-Control' in rv.headers and 'no-cache' in rv.headers['Cache-Control']

    def test_client_error(self, client):
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

    def test_client_error(self, client):
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

    def test_client_error(self, client):
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

    def test_client_error(self, client):
        rv = client.get('/cache/on_success_or_redirect/404')
        assert 'Cache-Control' not in rv.headers


class TestCacheVary:
    def test_success_wo_vary(self, client):
        rv = client.get('/cache/on_success/200')
        assert 'Vary' not in rv.headers

    def test_success(self, client):
        rv = client.get('/cache/vary/200')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_redirect(self, client):
        rv = client.get('/cache/vary/300')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_client_error(self, client):
        rv = client.get('/cache/vary/404')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR

    def test_server_error(self, client):
        rv = client.get('/cache/vary/500')
        assert rv.headers.get('Vary') == VARY_HEADERS_STR
