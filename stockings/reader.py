import datetime
import glob
import os

def get_stocks(path):
    """Finds comma-separated values in a path and, assuming they are
      named consistently, provides a dictionary with a stock symbol
      and its respective file name.
    :param path: string that is the directory to be search.
    :return: dictionary of stock symbols and their file name.
    """
    filenames = glob.glob('%s/*.csv' % (path, ))
    # TODO: verify naming scheme of CSV files (I don't have access RN)
    return {os.path.basename(x).split('.')[1]: x for x in filenames}


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
    if 'Key Statistics' in data[3]:
        stock['name'] = data[0][0].split('-')[0]
        stock['industry'] = data[1][1]
        stock['sector'] = data[1][2]
        stock['keystats'] = {}
        for line in data[4:10]:
            stock['keystats'][line[0]] = line[1]
        stock['growthrates'] = {}
        for line in data[12:17]:
            stock['growthrates'][line[0]] = line[1]

        stock['annual'] = {}
        stock['annual']['dates'] = [datetime.strptime('%b%Y', x) for x in data[20][1:31]]
        # Right now we skip the TTM/current since it doesn't follow the same month.
        #   To include it, uncomment the immedately following line and change the
        #   loop under it to extend to 32.
        #stock['annual']['dates'].append(datetime.strptime('%b%Y', 'Jan2017'))
        for line in data[21:]:
            stock['annual'][line[0]] = [float(x) for x in line[1:31]]

        stock['quarterly'] = {}
        stock['quarterly']['dates'] = [datetime.strptime('%b%Y', x) for x in data[20][33:]]
        for line in data[21]:
            stock['quarterly'][line[0]] = [float(x) for x in line[33:]]

        return stock
    else:
        raise Exception('File format not recognized or Ethan is bad.')
