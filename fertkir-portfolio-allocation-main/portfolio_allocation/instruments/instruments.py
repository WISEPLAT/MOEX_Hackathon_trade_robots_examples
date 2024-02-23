from .sources import currencies, funds, securities, custom


def get_data(tickers: list[str]) -> dict[str, dict]:
    info_by_currency = currencies.currencies(tickers)
    _currencies = info_by_currency.keys()
    not_currencies = list(filter(lambda ticker: ticker not in _currencies, tickers))
    info_by_fund = funds.funds(not_currencies)
    _funds = info_by_fund.keys()
    other = list(filter(lambda ticker: ticker not in _funds, not_currencies))
    _securities = securities.securities(other)
    result = info_by_currency | info_by_fund | _securities
    custom_info = custom.custom(tickers)
    for key, value in result.items():
        if key in custom_info.keys():
            value.update(custom_info[key])
    return result
