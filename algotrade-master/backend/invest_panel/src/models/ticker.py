from datetime import datetime

from .base import JSONModel, UUIDMixin, TimestampMixin


class TickerBrief(JSONModel, UUIDMixin):
    secid: str
    boardid: str
    shortname: str | None


class Ticker(TickerBrief, UUIDMixin, TimestampMixin):
    prevprice: float | None
    lotsize: int | None
    facevalue: float | None
    status: str | None
    boardname: str | None
    decimials: int | None
    secname: str| None
    remarks: str| None
    marketcode: str| None
    instrid: str| None
    sectorid: str| None
    minstep: float| None
    prevwaprice: float| None
    faceunit: str| None
    prevdate: datetime| None
    issuesize: int| None
    isin: str| None
    latname: str| None
    regnumber: str| None
    prevlegalcloseprice: float| None
    currencyid: str| None
    sectype: str| None
    listlevel: int| None
    settledate: datetime| None