import datetime
import glob
import os

def get_stocks(path):
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
        stock['annualinfo'] = {}
        stock['dates'] = [datetime.strptime('%b%Y', x) for x in data[20]]
        for line in data[21:]:
            stock[line[0]] = line[1:]

        return stock
    else:
        raise Exception('File format not recognized or Ethan is bad.')
