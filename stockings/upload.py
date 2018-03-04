"""
Upload stock data from the CSVs into the database.
"""

import itertools
import re
import sys

from config import from_config
from ringmaster import sql

import stockings


DOWNLOADED_DEFAULT = None
DEFAULT_CHUNKSIZE = 10000


def chunks(iterable, n):
    """Yield chunks of size n from an iterable."""
    # From https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def extract_numeric(v):
    """Extract a numeric value from a text field."""
    if type(v) not in {str, bytes}:
        return v
    match = re.search('\d+(\.\d+)*', v)
    if match:
        return float(match.group(0))
    return None  # Better default value? Nan?


class Uploader(object):

    def __init__(self, env, stocks, chunksize=DEFAULT_CHUNKSIZE):
        self.env = env
        self.stocks = stocks
        self.chunksize = chunksize

    def upload(self, uploads):
        """Upload data into selected tables."""
        for table_name in uploads:
            table = self.env.Table(table_name)
            records = getattr(self, '{table_name}_records'.format(table_name=table_name))()

            # Code gets killed for memory reasons if we don't chunk it
            for chunk in chunks(records, self.chunksize):
                self.env.conn.execute(table.insert(), chunk)

    def stock_records(self):
        """Get stock records from CSVs."""
        for stock, info in self.stocks.items():
            yield {
                'id': stock,
                'name': info['name'],
                'industry': info['industry'],
                'sector': info['sector']
            }

    def keystat_records(self):
        """Get keystat records from CSVs."""
        for stock, info in self.stocks.items():
            for stat, val in info['keystats'].items():
                yield {
                    'stock': stock,
                    'stat': stat,
                    'val': extract_numeric(val),
                    'downloaded': DOWNLOADED_DEFAULT
                }
        
    def growthrate_records(self):
        """Get growthrate records from CSVs."""
        for stock, info in self.stocks.items():
            for stat, val in info['growthrates'].items():
                yield {
                    'stock': stock,
                    'stat': stat,
                    'val': extract_numeric(val),
                    'downloaded': DOWNLOADED_DEFAULT
                }

    def annual_records(self):
        """Get annual records from CSVs."""
        for stock, info in self.stocks.items():
            dates = info['annual']['dates']
            for stat, series in info['annual'].items():
                if stat != 'dates':
                    for date, val in zip(dates, series):
                        yield {
                            'stock': stock,
                            'stat': stat,
                            'date': date,
                            'val': extract_numeric(val)
                        }

    def quarterly_records(self):
        """Get quarterly records from CSVs."""
        for stock, info in self.stocks.items():
            dates = info['quarterly']['dates']
            for stat, series in info['quarterly'].items():
                if stat != 'dates':
                    for date, val in zip(dates, series):
                        yield {
                            'stock': stock,
                            'stat': stat,
                            'date': date,
                            'val': extract_numeric(val)
                        }


def main(uploads, chunksize=DEFAULT_CHUNKSIZE):
    """Upload stock data from the CSVs into the database."""

    print("Loading stock data")
    stocks = stockings.reader.read_all_stocks()

    print("Uploading records")
    with sql.DatabaseEnvironment() as env:
        uploader = Uploader(env, stocks, chunksize=chunksize)
        uploader.upload(uploads)


if __name__ == '__main__':
    from_config(main)(sys.argv[1])
