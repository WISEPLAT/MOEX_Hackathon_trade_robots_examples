from django import forms
from Trading.models import stock
from . import models


class stockForm(forms.ModelForm):
    ticker = forms.CharField(label="Ticker", max_length=32)
    name = forms.CharField(label="Name", max_length=32)

   # name = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = models.stock
        fields = [
            "SECTYPE",
            "SECID",
            "LATNAME",
            "INSTRID",
            "REGNUMBER",
            "PREVPRICE",
            "FACEUNIT",
            "PREVLEGALCLOSEPRICE",
            "LISTLEVEL",
            "STATUS",
            "ISSUESIZE",
            "ISIN",
            "REMARKS",
            "PREVWAPRICE",
            "MINSTEP",
            "FACEVALUE",
            "MARKETCODE",
            "CURRENCYID",
            "SHORTNAME",
            "PREVDATE",
            "BOARDID",
            "LOTSIZE",
            "SECTORID",
            "BOARDNAME",
            "DECIMALS",
            "SECNAME",
            "SETTLEDATE",
        ]

"""        
        widgets = {
#            'ticker': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here'}),
            'ticker': forms.Textarea(attrs={'rows': 3}),
            'name': forms.Textarea(attrs={'rows': 3}),
        }
        """

class strategyForm(forms.ModelForm):
    class Meta:
        model = models.strategy
        fields = [
            "label",
        ]


class traderForm(forms.ModelForm):
    class Meta:
        model = models.trader
        fields = []

class tradestatForm(forms.ModelForm):
    class Meta:
        model = models.tradestat
        fields = [
            "SECID",
            "ts",
            "pr_open",
            "pr_high",
            "pr_low",
            "pr_close",
            "pr_change",
            "trades",
            "vol",
            "val",
            "pr_std",
            "disb",
            "pr_vwap",
            "trades_b",
            "vol_b",
            "val_b",
            "pr_vwap_b",
            "trades_s",
            "vol_s",
            "val_s",
            "pr_vwap_s",
        ]

    def __init__(self, *args, **kwargs):
        super(tradestatForm, self).__init__(*args, **kwargs)
        self.fields["stock"].queryset = stock.objects.all()