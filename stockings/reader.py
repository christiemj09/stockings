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
    # TODO: verify naming scheme of CSV files (I don't have access RN)
    return {os.path.basename(x).split('.')[0]: x for x in filenames}


def read_stock(path):
    """Reads in a comma-separated values file that contains stock
      information. The format is assumed to be our proprietary format.
    :param path: string that is the filename to be read
    :return: dictionary of stock information    
    """
    f = open(path, 'r')
    data = [x.split(',') for x in f.readlines()]
    f.close()

    stock = {}
    start = [ix for ix,x in enumerate(data) if 'Key Statistics' in x]
    if len(start) != 1:
        raise Exception('File format not recognized or Ethan is bad.')
    start = int(start[0])

    stock['name'] = data[0][0].split('-')[0].strip()
    stock['industry'] = data[1][1]
    stock['sector'] = data[1][2]
    stock['keystats'] = {}
    for line in data[start+1:start+7]:
        stock['keystats'][line[0]] = line[1]
    stock['growthrates'] = {}
    for line in data[start+9:start+14]:
        stock['growthrates'][line[0]] = line[1]

    floats = re.compile(u"^[-]?[0-9]+.[0-9]+$").search
    dates = re.compile(u"^[0-9]+/[0-9]+/[0-9]+$").search

    stock['annual'] = {}
    stock['annual']['dates'] = [datetime.datetime.strptime(x.strip('\r\n'), '%b%Y') for x in data[start+17][1:31]]
    # Right now we skip the TTM/current since it doesn't follow the same month.
    #   To include it, uncomment the immedately following line and change the
    #   loop under it to extend to 32.
    #stock['annual']['dates'].append(datetime.strptime('%b%Y', 'Jan2017'))
    for line in data[start+18:]:
        lstart = None
        for iv,value in enumerate(line):
            if floats(value):
                lstart = iv
                break
        if lstart:
            stock['annual'][line[0]] = [float(x.strip('\r\n')) if floats(x) else float('nan') for x in line[lstart:lstart+30]]
        else:
            # FIXME: handle data types besides floats; for now we ignore
            continue

    for key in stock['annual'].keys():
        assert len(stock['annual'][key]) == len(stock['annual']['dates'])

    stock['quarterly'] = {}
    stock['quarterly']['dates'] = [datetime.datetime.strptime(x.strip('\r\n'), '%b%Y') for x in data[start+17][33:]]
    for line in data[start+18:]:
        lstart = None
        for iv,value in enumerate(line):
            if floats(value):
                lstart = iv
                break
        if lstart:
            stock['quarterly'][line[0]] = [float(x.strip('\r\n')) if floats(x) else float('nan') for x in line[lstart+32:]]
        else:
            # FIXME: handle data types besides floats; for now we ignore
            continue

    for key in stock['quarterly'].keys():
         assert len(stock['quarterly'][key]) == len(stock['quarterly']['dates'])

    return stock
