from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from moexalgo import Market, Ticker, metrics
import pandas as pd
import datetime as dt
import pytz

from django.shortcuts               import render
from django.template                import RequestContext
from django.contrib.auth            import authenticate, login

class stockListView(generic.ListView):
    model = models.stock
    form_class = forms.stockForm

class stockCreateView(generic.CreateView):
    model = models.stock
    form_class = forms.stockForm


class stockDetailView(generic.DetailView):
    model = models.stock
    form_class = forms.stockForm


class stockUpdateView(generic.UpdateView):
    model = models.stock
    form_class = forms.stockForm
    pk_url_kwarg = "pk"


class stockDeleteView(generic.DeleteView):
    model = models.stock
    success_url = reverse_lazy("Trading_stock_list")


class strategyListView(generic.ListView):
    model = models.strategy
    form_class = forms.strategyForm


class strategyCreateView(generic.CreateView):
    model = models.strategy
    form_class = forms.strategyForm


class strategyDetailView(generic.DetailView):
    model = models.strategy
    form_class = forms.strategyForm


class strategyUpdateView(generic.UpdateView):
    model = models.strategy
    form_class = forms.strategyForm
    pk_url_kwarg = "pk"


class strategyDeleteView(generic.DeleteView):
    model = models.strategy
    success_url = reverse_lazy("Trading_strategy_list")

class traderListView(generic.ListView):
    model = models.trader
    form_class = forms.traderForm

class traderCreateView(generic.CreateView):
    model = models.trader
    form_class = forms.traderForm


class traderDetailView(generic.DetailView):
    model = models.trader
    form_class = forms.traderForm


class traderUpdateView(generic.UpdateView):
    model = models.trader
    form_class = forms.traderForm
    pk_url_kwarg = "pk"


class traderDeleteView(generic.DeleteView):
    model = models.trader
    success_url = reverse_lazy("Trading_trader_list")


class tradestatListView(generic.ListView):
    model = models.tradestat
    form_class = forms.tradestatForm


class tradestatCreateView(generic.CreateView):
    model = models.tradestat
    form_class = forms.tradestatForm


class tradestatDetailView(generic.DetailView):
    model = models.tradestat
    form_class = forms.tradestatForm


class tradestatUpdateView(generic.UpdateView):
    model = models.tradestat
    form_class = forms.tradestatForm
    pk_url_kwarg = "pk"


class tradestatDeleteView(generic.DeleteView):
    model = models.tradestat
    success_url = reverse_lazy("Trading_trading_history_list")

class tradestatImportFromAPI():
    mtradestat = models.tradestat
    stocks = models.stock

    """
#    stock.values("SECID")
    tickers = stocks.objects.values("SECID")

#    tickers = stocks.from_db(field_names=["SECID"])
#    print(tickers)
    for sticker in tickers:
        ticker = Ticker(sticker['SECID'])
        end_date = dt.datetime.today()
        timestamp_now = dt.datetime.timestamp(end_date)
        timestamp_start = dt.datetime.fromtimestamp(timestamp_now - 604800)
        timestamp_start = timestamp_start.strftime("%Y-%m-%d")
        xtradestat = pd.DataFrame(ticker.tradestats(date=timestamp_start, till_date='today'))

        for x in xtradestat.iterrows():
            print(x[1])

            mtradestat.objects.create(
                stock = stocks.objects.filter(SECID=x[1]['secid'])[0],
                SECID = x[1]['secid'],
                ts = pytz.timezone('Europe/Moscow').localize(x[1]['ts'], is_dst=None),
                pr_open = x[1]['pr_open'],
                pr_high = x[1]['pr_high'],
                pr_low = x[1]['pr_low'],
                pr_close = x[1]['pr_close'],
                pr_change = x[1]['pr_change'],
                trades = x[1]['trades'],
                vol = x[1]['vol'],
                val = x[1]['val'],
                pr_std = x[1]['pr_std'],
                disb = x[1]['disb'],
                pr_vwap = x[1]['pr_vwap'],
                trades_b = x[1]['trades_b'],
                vol_b = x[1]['vol_b'],
                val_b = x[1]['val_b'],
                pr_vwap_b = x[1]['pr_vwap_b'],
                trades_s = x[1]['trades_s'],
                vol_s = x[1]['vol_s'],
                val_s = x[1]['val_s'],
                pr_vwap_s = x[1]['pr_vwap_s']
            )
    """

# out = tradestat.to_json(orient='records', force_ascii=False)
# tradestat.to_csv('trading.csv', sep='\t', encoding='utf-8')

    success_url = reverse_lazy("Trading_trading_history_list")

def tradestatBySECID(request, SECID):
    tradestat = models.tradestat
    tradestatOfSECID = tradestat.objects.filter(SECID = SECID)
    print(tradestat)
    return render(request, 'Trading/tradestat_SECID_list.html', locals())

#    return render(request, 'Trading/tradestat_SECID.html', context_instance=RequestContext(request))

