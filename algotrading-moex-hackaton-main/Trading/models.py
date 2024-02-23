import datetime

from django.db import models
from django.urls import reverse
from datetime import timezone

class stock(models.Model):

    # Fields
#    ticker = models.CharField(max_length=10)
#    created = models.DateTimeField(auto_now_add=True, editable=False)
#    last_updated = models.DateTimeField(auto_now=True, editable=False)
#    name = models.CharField(max_length=60)
    SECID = models.CharField(max_length=10, default='')
    BOARDID = models.CharField(max_length=10, default='')
    SHORTNAME = models.CharField(max_length=10, default='')
    PREVPRICE = models.FloatField( default=0)
    LOTSIZE = models.IntegerField( default=0)
    FACEVALUE = models.FloatField( default=0)
    STATUS = models.CharField(max_length=4, default='')
    BOARDNAME = models.CharField(max_length=30, default='')
    DECIMALS = models.IntegerField(default=0)
    SECNAME = models.CharField(max_length=30, default='')
    REMARKS = models.CharField(max_length=10, default='')
    MARKETCODE = models.CharField(max_length=10, default='')
    INSTRID = models.CharField(max_length=10, default='')
    SECTORID = models.CharField(max_length=10, default='')
    MINSTEP = models.FloatField(default=0)
    PREVWAPRICE = models.FloatField(default=0)
    FACEUNIT = models.CharField(max_length=10, default='')
    PREVDATE = models.DateField(blank=True)
    ISSUESIZE = models.BigIntegerField(default=0)
    ISIN = models.CharField(max_length=20, default='')
    LATNAME = models.CharField(max_length=10, default='')
    REGNUMBER = models.CharField(max_length=20, default='')
    PREVLEGALCLOSEPRICE = models.FloatField(default=0)
    CURRENCYID = models.CharField(max_length=10, default='')
    SECTYPE = models.CharField(max_length=10, default='')
    LISTLEVEL = models.IntegerField(default=0)
    SETTLEDATE = models.DateField(blank=True)

    """
        "SECID": "ABIO",
        "BOARDID":"TQBR",
        "SHORTNAME": "iАРТГЕН ао",
        "PREVPRICE": 88.1,
        "LOTSIZE": 10,
        "FACEVALUE": 0.1,
        "STATUS": "A",
        "BOARDNAME": "Т+: Акции и ДР - безадрес.",
        "DECIMALS": 2,
        "SECNAME": "ПАО \"Артген\"",
        "REMARKS": "None",
        "MARKETCODE": "FNDT",
        "INSTRID": "EQIN",
        "SECTORID": "None",
        "MINSTEP": 0.02,
        "PREVWAPRICE": 88.62,
        "FACEUNIT": "SUR",
        "PREVDATE": 1701734400000,
        "ISSUESIZE": 92645451,
        "ISIN": "RU000A0JNAB6",
        "LATNAME": "ARTGEN ao",
        "REGNUMBER": "1-01-08902-A",
        "PREVLEGALCLOSEPRICE": 88.1,
        "CURRENCYID": "SUR",
        "SECTYPE": "1",
        "LISTLEVEL": 2,
        "SETTLEDATE": 1701907200000
    """

    class Meta:
        pass

    def __str__(self):
#       return f"{self.createdAt.strftime('%d-%m-%Y')}"
        return f"{self.SHORTNAME}"

    def get_absolute_url(self):
        return reverse("Trading_stock_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Trading_stock_update", args=(self.pk,))


class strategy(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    label = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Trading_strategy_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Trading_strategy_update", args=(self.pk,))



class trader(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Trading_trader_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Trading_trader_update", args=(self.pk,))


class tradestat(models.Model):

    # Relationships
    stock = models.ForeignKey(stock, related_name="stocksData", on_delete=models.CASCADE)

    # Fields
#    priceUpdateDateTime = models.DateTimeField()
#    last_updated = models.DateTimeField(auto_now=True, editable=False)
#    price = models.FloatField()
#    created = models.DateTimeField(auto_now_add=True, editable=False)

    SECID = models.CharField(max_length=10, default='')
    ts = models.DateTimeField()
    pr_open = models.FloatField(blank=True)
    pr_high = models.FloatField(blank=True)
    pr_low = models.FloatField(blank=True)
    pr_close = models.FloatField(blank=True)
    pr_change = models.FloatField(blank=True)
    trades = models.IntegerField()
    vol = models.IntegerField()
    val = models.FloatField(blank=True)
    pr_std = models.FloatField(blank=True)
    disb = models.FloatField(blank=True)
    pr_vwap = models.FloatField(blank=True)
    trades_b = models.IntegerField()
    vol_b = models.IntegerField()
    val_b = models.FloatField(blank=True)
    pr_vwap_b = models.FloatField(blank=True)
    trades_s = models.IntegerField()
    vol_s = models.IntegerField()
    val_s = models.FloatField(blank=True)
    pr_vwap_s = models.FloatField(blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Trading_tradestat_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Trading_tradestat_update", args=(self.pk,))