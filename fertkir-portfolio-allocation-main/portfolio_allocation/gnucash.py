import re
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class ParsedGnuCashReport:
    title: str
    currency: str
    value_by_instrument: dict[str, float]


class ParseException(Exception):
    pass


class CannotRunGnuCash(Exception):
    pass


def get_value_by_instrument(report_name: str, datafile: str) -> ParsedGnuCashReport:
    proc = _try_run_gnucash_cli(['--report', 'run', '--name=' + report_name, datafile])
    return parse_value_by_instrument(proc.stdout.read().decode('utf-8'))


def _try_run_gnucash_cli(params: [str]):
    cmd_list = [['gnucash-cli'], ['flatpak', 'run', '--command=gnucash-cli', 'org.gnucash.GnuCash']]
    for cmd in cmd_list:
        try:
            cmd.extend(params)
            return subprocess.Popen(cmd, stdout=subprocess.PIPE)
        except:
            continue
    raise CannotRunGnuCash()


def parse_value_by_instrument(html_report: str) -> ParsedGnuCashReport:
    labels_match = re.search('"labels"\\s*:\\s*\\[\\s*"(.*)"\\s*],', html_report)
    if labels_match is None:
        raise ParseException("Could not find chart's labels in GnuCash's report")
    labels = re.split('"\\s*,\\s*"', labels_match.group(1))
    instruments = [re.split('\\s*-\\s*', label)[0] for label in labels]
    volumes = list(
        map(float, re.split('\\s*,\\s*', re.search('"data"\\s*:\\s*\\[\\s*(.*)\\s*],', html_report).group(1))))
    currency = re.search('var\\s+curriso\\s*=\\s*"(.*)"\\s*;', html_report).group(1)
    title = re.search('"text"\\s*:\\s*\\[\\s*"(.*)"\\s*,\\s*"(.*)"\\s*]', html_report).group(1)
    return ParsedGnuCashReport(title, currency, dict(zip(instruments, volumes)))


def get_latest_file():
    # from https://github.com/sdementen/gnucash-utilities/blob/develop/piecash_utilities/config.py
    if sys.platform.startswith("linux"):
        import subprocess
        try:
            output_dconf = subprocess.check_output(["dconf", "dump", "/org/gnucash/GnuCash/history/"]).decode()
            from configparser import ConfigParser
            conf = ConfigParser()
            conf.read_string(output_dconf)
            return conf["/"]["file0"][1:-1]
        except:
            return None
    else:
        return None
