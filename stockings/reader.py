import csv
import datetime
import glob
import os
import re

def get_stocks(path):
    """Finds comma-separated values in a path and, assuming they are
      named consistently, provides a dictionary with a stock symbol
      and its respective file name.
    :param path: string that is the directory to be search.
    :return: dictionary of stock symbols and their file name.
    """
    filenames = glob.glob('%s/*.csv' % (path, ))
    return {os.path.basename(x).split('.')[0]: x for x in filenames}


def read_stock(path):
    """Reads in a comma-separated values file that contains stock
      information. The format is assumed to be our proprietary format.
    :param path: string that is the filename to be read
    :return: dictionary of stock information    
    """
    f = open(path, 'r')
    data = csv.reader(f, delimiter=',')
    data = [x for x in data]
    if len(data) != 213:
        return {}

    stock = {}

    # We make sure the data follows our standard format
    if 'Key Statistics' not in data[3]:
        raise Exception('File format not recognized or Ethan is bad.')
    start = 3

    # Get summary information of the stock
    stock['name'] = data[0][0].split('-')[0].strip()
    stock['industry'] = data[1][1]
    stock['sector'] = data[1][2]
    stock['keystats'] = {}
    for line in data[start+1:start+7]:
        stock['keystats'][line[0].lstrip().rstrip()] = line[1]
    stock['growthrates'] = {}
    for line in data[start+9:start+14]:
        stock['growthrates'][line[0].lstrip().rstrip()] = line[1]

    # Set up regex patterns for type testing
    floats = re.compile(u"^[-]?[0-9]+.[0-9]+$").search
    dates = re.compile(u"^[0-9]+/[0-9]+/[0-9]+$").search

    # Parse annual data
    stock['annual'] = {}
    stock['annual']['dates'] = [datetime.datetime.strptime(x.strip('\r\n'), '%b%Y') for x in data[start+17][1:31]]
    # Right now we skip the TTM/current since it doesn't follow the same month.
    #   To include it, uncomment the immedately following line and change the
    #   loop under it to extend to 32.
    #stock['annual']['dates'].append(datetime.strptime('%b%Y', 'Jan2017'))
    for line in data[start+18:]:
        stock['annual'][line[0].lstrip().rstrip()] = [float(x.strip('\r\n')) if floats(x) else float('nan') for x in line[1:31]]

    # Parse quarterly data
    stock['quarterly'] = {}
    stock['quarterly']['dates'] = [datetime.datetime.strptime(x.strip('\r\n'), '%b%Y') for x in data[start+17][33:]]
    for line in data[start+18:]:
        stock['quarterly'][line[0].lstrip().rstrip()] = [float(x.strip('\r\n')) if floats(x) else float('nan') for x in line[33:]]

    return stock


def read_all_stocks():
    stocks = get_stocks('./csv_stock_data/')

    stock_data = {}

    for stock in stocks:
        stock_data[stock] = read_stock(stocks[stock])

        # Handle bad files that return an empty dictionary
        if len(stock_data[stock].keys()) == 0:
            stock_data.pop(stock)

    return stock_data
