import json
import os

from ..model import InstrumentDataSource

_SECURITIES_CUSTOM_JSON = os.path.join(
    os.environ.get('APPDATA') or
    os.environ.get('XDG_CONFIG_HOME') or
    os.path.join(os.environ['HOME'], '.config'),
    "portfolio-allocation",
    "securities-custom.json"
)


class CustomDataSource(InstrumentDataSource):
    def get(self, instruments: list[str]) -> dict[str, dict]:
        if not os.path.exists(_SECURITIES_CUSTOM_JSON):
            print("No custom config \"" + _SECURITIES_CUSTOM_JSON + "\", ignoring it")
            return {}
        print("Reading custom config \"" + _SECURITIES_CUSTOM_JSON + "\"")
        f = open(_SECURITIES_CUSTOM_JSON, "r")
        configs = json.loads(f.read())
        result = {}
        for config in configs:
            instrument_in_config = config['instrument']
            if instrument_in_config == '*':
                for i in instruments:
                    result[i] = config.copy()
                    result[i]['instrument'] = i
            elif instrument_in_config.endswith('*'):
                for i in instruments:
                    if i.startswith(instrument_in_config[:-1]):
                        result[i] = config.copy()
                        result[i]['instrument'] = i
            elif instrument_in_config in instruments:
                result[instrument_in_config] = config.copy()
        return result


custom = CustomDataSource().get
