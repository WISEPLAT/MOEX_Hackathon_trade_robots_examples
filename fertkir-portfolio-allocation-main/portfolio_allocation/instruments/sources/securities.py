import sys
import time
from dataclasses import asdict

import pycountry
import yfinance
from cache_to_disk import cache_to_disk

from portfolio_allocation.instruments.model import InstrumentData, InstrumentDataSource

_DEFAULT_CACHE_AGE = 30
_DEFAULT_EXCHANGE = "ME"  # todo parameterize it in some other way


class SecurityDataSource(InstrumentDataSource):
    def get(self, instruments: list[str]) -> dict[str, dict]:
        result = {}
        for instrument in instruments:
            try:
                result[instrument] = _yahoo(instrument,
                    instrument if instrument.__contains__(".") else instrument + "." + _DEFAULT_EXCHANGE)
            except _InstrumentMissingException:
                print('No data for ticker "' + instrument + '", allocation report will not reflect it', file=sys.stderr)
                continue
        return result

@cache_to_disk(_DEFAULT_CACHE_AGE)
def _yahoo(instrument: str, instrument_with_exchange: str) -> dict:
    print("Sending request to Yahoo Finance for " + instrument)
    start = time.time()
    info = yfinance.Ticker(instrument_with_exchange).get_info()
    print("Got response in " + str(time.time() - start) + " seconds")
    if info.get('quoteType') is None:
        raise _InstrumentMissingException
    info_keys = info.keys()
    return asdict(InstrumentData(
        instrument=instrument,
        countries={
            pycountry.countries.get(alpha_2='RU').name: 1  # todo it must not be always RU
        },
        industries=None if 'sector' not in info_keys else {
            info['sector']: 1
        },
        fee=0,
        currencies=None if 'financialCurrency' not in info_keys else {
            info['financialCurrency']: 1
        },
        classes=None if 'quoteType' not in info_keys else {
            info['quoteType']: 1
        }
    ))


class _InstrumentMissingException(Exception):
    pass


securities = SecurityDataSource().get
