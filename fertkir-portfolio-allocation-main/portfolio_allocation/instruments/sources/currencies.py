from dataclasses import asdict

import pycountry

from ..model import InstrumentData, InstrumentDataSource


class CurrencyDataSource(InstrumentDataSource):
    def get(self, instruments: list[str]) -> dict[str, dict]:
        result = {}
        for currency_code in instruments:
            currency = pycountry.currencies.get(alpha_3=currency_code)
            if currency is None:
                continue
            result[currency_code] = asdict(InstrumentData(
                instrument=currency_code,
                countries={
                    self._to_country(currency.alpha_3): 1
                },
                industries={},
                fee=0,
                currencies={
                    currency.alpha_3: 1
                },
                classes={
                    'Cash': 1
                }
            ))
        return result

    @staticmethod
    def _to_country(currency: str) -> str:
        return 'Europe' if currency == 'EUR' else pycountry.countries.get(alpha_2=currency[0:2]).name


currencies = CurrencyDataSource().get
