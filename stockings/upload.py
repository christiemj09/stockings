"""
Upload stock data from the CSVs into the database.
"""

import re
import sys

from config import from_config
from ringmaster import sql

import stockings


DOWNLOADED_DEFAULT = None


def extract_numeric(v):
    """Extract a numeric value from a text field."""
    return v if type(v) is float else float(re.search('\d+(\.\d+)*', v).group(0))


class Uploader(object):

    def __init__(self, env, stocks):
        self.env = env
        self.stocks = stocks

    def upload(self, uploads):
        """Upload data into selected tables."""
        for table_name in uploads:
            table = self.env.Table(table_name)
            records = getattr(self, '{table_name}_records')()
            self.env.conn.execute(table.insert(), list(records))  # chunk these eventually?

    def stock_records(self):
        """Get stock records from CSVs."""
        for stock, info in self.stocks.items():
            yield stock, info['name'], info['industry'], info['sector']

    def keystat_records(self):
        """Get keystat records from CSVs."""
        for stock, info in self.stocks.items():
            for stat, val in info['keystats'].items():
                yield stock, stat, extract_numeric(val), DOWNLOADED_DEFAULT
        
    def growthrate_records(self):
        """Get growthrate records from CSVs."""
        for stock, info in self.stocks.items():
            for stat, val in info['growthrates'].items():
                yield stock, stat, extract_numeric(val), DOWNLOADED_DEFAULT

    def annual_records(self):
        """Get annual records from CSVs."""
        for stock, info in self.stocks.items():
            dates = info['annual']['dates']
            for stat, series in info['annual'].items():
                for date, val in zip(dates, series):
                    yield stock, stat, date, extract_numeric(val)

    def quarterly_records(self):
        """Get quarterly records from CSVs."""
        for stock, info in self.stocks.items():
            dates = info['quarterly']['dates']
            for stat, series in info['quarterly'].items():
                for date, val in zip(dates, series):
                    yield stock, stat, date, extract_numeric(val)


def main(uploads):
    """Upload stock data from the CSVs into the database."""

    print("Loading stock data")
    stocks = stockings.reader.read_all_stocks()
    
    with sql.DatabaseEnvironment() as env:
        uploader = Uploader(env, stocks)
        uploader.upload(uploads)


if __name__ == '__main__':
    from_config(main)(sys.arg[1])
