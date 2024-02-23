from django.contrib import admin
from django import forms

from . import models


class stockAdminForm(forms.ModelForm):

    class Meta:
        model = models.stock
        fields = "__all__"


class stockAdmin(admin.ModelAdmin):
    form = stockAdminForm
    list_display = [
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
#        "created",
#        "last_updated",
    ]
    readonly_fields = [
#        "created",
#        "last_updated",
#        "ticker",
#        "name",
    ]

class strategyAdminForm(forms.ModelForm):

    class Meta:
        model = models.strategy
        fields = "__all__"


class strategyAdmin(admin.ModelAdmin):
    form = strategyAdminForm
    list_display = [
        "last_updated",
        "created",
        "label",
    ]
    readonly_fields = [
        "last_updated",
        "created",
        "label",
    ]


class traderAdminForm(forms.ModelForm):

    class Meta:
        model = models.trader
        fields = "__all__"


class traderAdmin(admin.ModelAdmin):
    form = traderAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class tradestatAdminForm(forms.ModelForm):

    class Meta:
        model = models.tradestat
        fields = "__all__"


class tradestatAdmin(admin.ModelAdmin):
    form = tradestatAdminForm
    list_display = [
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
    readonly_fields = [
#        "priceUpdateDateTime",
#        "last_updated",
#        "price",
#        "created",
    ]


admin.site.register(models.stock, stockAdmin)
admin.site.register(models.strategy, strategyAdmin)
admin.site.register(models.trader, traderAdmin)
admin.site.register(models.tradestat, tradestatAdmin)
