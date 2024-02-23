from typing import Any, Iterator

from src.transform.base import BaseTransformer
from src.models.ticker import TickerModel, TickerBriefModel


class TickerBriefTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = TickerBriefModel(
                secid=elem.get('SECID') or elem.get('secid')
            )
            yield elem.model_dump() if to_dict else elem


class TickerTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = TickerModel(
                secid=elem.get('SECID'),
                boardid=elem.get('BOARDID'),
                shortname=elem.get('SHORTNAME'),
                prevprice=elem.get('PREVPRICE'),
                lotsize=elem.get('LOTSIZE'),
                facevalue=elem.get('FACEVALUE'),
                status=elem.get('STATUS'),
                boardname=elem.get('BOARDNAME'),
                decimials=elem.get('DECIMIALS'),
                secname=elem.get('SECNAME'),
                remarks=elem.get('REMARKS'),
                marketcode=elem.get('MARKETCODE'),
                instrid=elem.get('INSTRID'),
                sectorid=elem.get('SECTORID'),
                minstep=elem.get('MINSTEP'),
                prevwaprice=elem.get('PREVWAPRICE'),
                faceunit=elem.get('FACEUNIT'),
                prevdate=elem.get('PREVDATE'),
                issuesize=elem.get('ISSUESIZE'),
                isin=elem.get('ISIN'),
                latname=elem.get('LATNAME'),
                regnumber=elem.get('REGNUMBER'),
                prevlegalcloseprice=elem.get('PREVLEGALCLOSEPRICE'),
                currencyid=elem.get('CURRENCYID'),
                sectype=elem.get('SECTYPE'),
                listlevel=elem.get('LISTLEVEL'),
                settledate=elem.get('SETTLEDATE'),
            )
            yield elem.model_dump() if to_dict else elem
