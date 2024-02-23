from dataclasses import dataclass


@dataclass
class InstrumentData:
    instrument: str
    countries: dict[str, float]
    industries: dict[str, float]
    fee: float
    currencies: dict[str, float]
    classes: dict[str, float]


class InstrumentDataSource:
    def get(self, instruments: list[str]) -> dict[str, dict]:
        pass
