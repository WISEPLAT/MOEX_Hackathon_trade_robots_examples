# Portfolio Allocation for GnuCash
Currency, country, asset class and industry allocations for portfolio of ETFs and mutual funds

What the program does:
1. Takes instrument allocation from [GnuCash's "Security" pie chart report](https://raw.githack.com/fertkir/portfolio-allocation/master/examples/gnucash.html)
2. Fetches data for each instrument from the Internet:
   1. Finex website
   2. Tinkoff website
   3. Yahoo Finance
3. Generates and opens [portfolio allocation report](https://raw.githack.com/fertkir/portfolio-allocation/master/examples/allocation.html) in your browser.

## Installation
```commandline
pip install portfolio-allocation
```

## Usage
To generate report based on default "Securities" GnuCash report for recently open GnuCash file:
```commandline
portfolio-allocation gnucash
```
But you'd better customize it, since the "Securities" pie chart is limited to 7 instruments:
```commandline
portfolio-allocation gnucash -r MyCustomReport1 MuCustomReport2
```
To select another GnuCash file:
```commandline
portfolio-allocation gnucash -r MyCustomReport -f /home/user/other.gnucash
```

To view all the possible options, check:
```commandline
portfolio-allocation -h
```

