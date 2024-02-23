import json
import locale
import os
import tempfile
import webbrowser
from importlib import resources as pkg_resources
from os.path import expanduser, dirname, realpath, join, exists

import requests

from . import resources
from .. import instruments

_CHART_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.2.1/chart.umd.min.js'
_CACHE_DIR = expanduser(join(dirname(realpath(__file__)), 'cache'))
_CHART_JS_CACHE_FILE = expanduser(join(_CACHE_DIR, 'chart.js'))
_MAIN_JS_FILE = expanduser(join(dirname(realpath(__file__)), 'resources/main.js'))
_MAIN_CSS_FILE = expanduser(join(dirname(realpath(__file__)), 'resources/main.css'))
_DEFAULT_LOCALE = locale.getlocale()[0].replace('_', '-')
try:
    locale.setlocale(locale.LC_ALL, '')
    _DEFAULT_CURRENCY = locale.localeconv().get('int_curr_symbol').strip()
except:
    _DEFAULT_CURRENCY = 'USD'


def generate(title: str,
             value_by_ticker: dict[str, float],
             currency: str = _DEFAULT_CURRENCY,
             user_locale: str = _DEFAULT_LOCALE):
    data_by_ticker = instruments.get_data(list(value_by_ticker.keys()))
    data = []
    for key, value in data_by_ticker.items():
        value['quantity'] = value_by_ticker[key]
        data.append(value)
    _generate_report(title, currency, user_locale, data)


def _generate_report(title: str, currency: str, user_locale: str, data: list[dict]):
    _ensure_chart_js_downloaded()
    report = pkg_resources.read_text(resources, 'report_template.html') \
        .replace('%DATA%', json.dumps(data)) \
        .replace('%CHART_JS%', _CHART_JS_CACHE_FILE) \
        .replace('%MAIN_JS%', _MAIN_JS_FILE) \
        .replace('%MAIN_CSS%', _MAIN_CSS_FILE) \
        .replace('%CURRENCY%', currency) \
        .replace('%LOCALE%', user_locale) \
        .replace('%TITLE%', title)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        file.write(report)
        webbrowser.open('file://' + file.name)


def _ensure_chart_js_downloaded():
    if exists(_CHART_JS_CACHE_FILE):
        return
    os.makedirs(name=_CACHE_DIR, mode=0o755, exist_ok=True)
    with open(_CHART_JS_CACHE_FILE, 'w') as file:
        file.write(requests.get(_CHART_JS_URL).text)
