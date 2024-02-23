import json

from django.views import View

from django.http import JsonResponse

from market.models import Ticket, Profile
from moexalgo import Ticker
import datetime
import numpy as np


TICKERS = [
                {
                    "name": "МосБиржа",
                    "code": "MOEX"
                },
                {
                    "name": "МТС-ао",
                    "code": "MTSS"
                },
                {
                    "name": "Сбербанк",
                    "code": "SBER"
                },
                {
                    "name": "Алроса",
                    "code": "ALRS"
                }
            ]

# ['NKNC', 'MRKC', 'GMKN', 'ALRS', 'GCHE', 'MAGN', 'ELFV', 'AKRN']


class ProfileBalanceJSONView(View):

    def calculate_sma(self, data, window_size):
        result = []
        for i in range(len(data)):
            if i < window_size:
                result.append(np.mean(data[:i + 1]))
            else:
                result.append(np.mean(data[i - window_size:i + 1]))
        return result


    def get(self, request):
        ticker_code = request.session.get('analytics', {}).get('ticker', 'SBER')
        ma_s = request.session.get('analytics', {}).get('param1', 5)
        ma_l = request.session.get('analytics', {}).get('param2', 20)
        print(request.session['analytics'])
        ticker = Ticker(ticker_code)
        start_date = datetime.datetime.now() - datetime.timedelta(days=367)
        end_date = datetime.datetime.now() - datetime.timedelta(days=365)
        candels = ticker.candles(date=start_date.date().isoformat(), till_date=end_date.date().isoformat(), period='1h')
        raw_result = {}
        for i in candels:
            candle_date_and_hour = i.end.strftime("%Y-%m-%d %H")
            raw_result[candle_date_and_hour] = (i.high + i.low) / 2

        return JsonResponse(
            {
                "income": -20,
                "total": 887234,
                "tickers": [
                    {
                        "name": [i for i in TICKERS if i['code'] == ticker_code][0]["name"],
                        "code": ticker_code
                    }
                ],
                "analytics": {
                    "labels": list(raw_result.keys()),
                    "datasets": [
                        {
                            "label": [i for i in TICKERS if i['code'] == ticker_code][0]["name"],
                            "data": list(raw_result.values())
                        },
                        {
                            "label": "скользящее среднее 1",
                            "data": self.calculate_sma(list(raw_result.values()), ma_s)
                        },
                        {
                            "label": "скользящее среднее 2",
                            "data": self.calculate_sma(list(raw_result.values()), ma_l)
                        }
                    ]
                }
            }
        )


class AllTicketsJSONView(View):

    def get(self, request):
        # tickets = Ticket.objects.all()
        # tickets_data = []
        # for ticket in tickets:
        #     tickets_data.append({
        #         'name': ticket.name,
        #         'code': ticket.code,
        #     })
        return JsonResponse(
            TICKERS, safe=False
        )


class AnalyticsView(View):

    def post(self, request):
        session = request.session
        session['analytics'] = json.loads(request.body)
        return JsonResponse({})