import numpy as np
import pandas as pd


def insider_watcher(obj, ws=False):
    for row in dir(obj):
        print row
    print 'And Type is {}'.format(type(obj))
    if ws:
        print obj
    return 0


def dict_watcher(dic):
    for key in dic:
        print key, dic[key]
    return 0


if __name__ == '__main__':
    print 'its main'
    l_src_dir = './ml-latest-small/ml-latest-small/'
    ratings = pd.read_csv(l_src_dir + 'ratings.csv', header=0)
    movies = pd.read_csv(l_src_dir + 'movies.csv', header=0)

    print ratings.rating.size
    count = 0
    for row in ratings.userId[range(ratings.rating.size)]:
        print row
        count += 1

    print count


