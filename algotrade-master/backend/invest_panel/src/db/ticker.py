from datetime import datetime
from sqlalchemy import String, Column, Integer, Float, BigInteger, TIMESTAMP

from .base import BaseModel


class Ticker(BaseModel):

    secid: str = Column(String(256), nullable=False)
    boardid: str = Column(String(256), nullable=False)
    shortname: str = Column(String(4096), nullable=True)
    prevprice: float = Column(Float, nullable=True)
    lotsize: int = Column(BigInteger, nullable=True)
    facevalue: float = Column(Float, nullable=True)
    status: str = Column(String(4096), nullable=True)
    boardname: str = Column(String(4096), nullable=True)
    decimials: int = Column(Integer, nullable=True)
    secname: str = Column(String(4096), nullable=True)
    remarks: str = Column(String(4096), nullable=True)
    marketcode: str = Column(String(4096), nullable=True)
    instrid: str = Column(String(4096), nullable=True)
    sectorid: str = Column(String(4096), nullable=True)
    minstep: float = Column(Float, nullable=True)
    prevwaprice: float = Column(Float, nullable=True)
    faceunit: str = Column(String(4096), nullable=True)
    prevdate: datetime = Column(TIMESTAMP(timezone=True), nullable=True)
    issuesize: int = Column(BigInteger, nullable=True)
    isin: str = Column(String(4096), nullable=True)
    latname: str = Column(String(4096), nullable=True)
    regnumber: str = Column(String(4096), nullable=True)
    prevlegalcloseprice: float = Column(Float, nullable=True)
    currencyid: str = Column(String(4096), nullable=True)
    sectype: str = Column(String(4096), nullable=True)
    listlevel: int = Column(Integer, nullable=True)
    settledate: datetime = Column(TIMESTAMP(timezone=True), nullable=True)
