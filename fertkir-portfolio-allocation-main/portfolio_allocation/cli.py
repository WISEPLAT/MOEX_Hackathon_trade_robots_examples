import argparse
import json
import os
import sys

from . import instruments, gnucash, report

_DEFAULT_REPORT_NAME_ENV_VAR = 'PORTFOLIO_ALLOCATION_GNUCASH_REPORT'


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands', help='Commands description', required=True)

    asset_data = subparsers.add_parser('tickerdata',
                                       help='Shows currency, fee, allocation data for provided list of tickers')
    asset_data.set_defaults(cmd='tickerdata')
    asset_data.add_argument('tickers', metavar='ticker', type=str, nargs='+',
                            help='a ticker of an asset to get info for')

    asset_allocation_gnucash = subparsers.add_parser(
        'gnucash',
        help='Generates allocation report based on GnuCash\'s Security Piechart and allocation data of its components')
    asset_allocation_gnucash.set_defaults(cmd='gnucash')
    asset_allocation_gnucash.add_argument(
        "-r", "--report-names",
        help="Name of report which contains securities allocation. Default: Securities",
        nargs='+', type=str,
        default=[os.environ.get(_DEFAULT_REPORT_NAME_ENV_VAR, 'Securities')])

    default_datafile = gnucash.get_latest_file()
    if default_datafile is None:
        asset_allocation_gnucash.add_argument("-f", "--datafile", required=True, type=str,
                                              help="GnuCash datafile (.gnucash)")
    else:
        asset_allocation_gnucash.add_argument(
            "-f", "--datafile",
            help="GnuCash datafile (.gnucash). Default: " + default_datafile,
            nargs='?', const=1, type=str,
            default=default_datafile)

    args = parser.parse_args()

    if args.cmd == 'tickerdata':
        print(json.dumps(instruments.get_data(args.tickers), indent=2, ensure_ascii=False))
    elif args.cmd == 'gnucash':
        for report_name in args.report_names:
            try:
                parsed_gnucash_report = gnucash.get_value_by_instrument(report_name=report_name, datafile=args.datafile)
                report.generate(parsed_gnucash_report.title,
                                parsed_gnucash_report.value_by_instrument,
                                parsed_gnucash_report.currency)
            except gnucash.ParseException as e:
                print(e, file=sys.stderr)


if __name__ == '__main__':
    main()
