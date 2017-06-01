import numpy as np
import pandas as pd
import re
import sys


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


def ret_y_mn(mvn='Hl (aa) and (122) this a; (1923)'):
    patt = re.compile(u'\d{4}\D*$')
    res_re_p = re.search(patt, mvn)
    if not res_re_p:
        print mvn
        print 'match failed, and failed info is above'
        return 0
    patt2 = re.compile(u'\d*')
    resrep = re.search(patt2, res_re_p.group())
    return int(resrep.group())


def mv_year_divide(mvns):
    titles = mvns.values
    myd_dic = {'1950-': 0, '1950+': 0, '1970+': 0, '1990+': 0, '2010+': 0}
    for ys in titles:
        ysi = ret_y_mn(ys)
        if ysi > 2010:
            myd_dic['2010+'] += 1
            continue
        if ysi > 1990:
            myd_dic['1990+'] += 1
            continue
        if ysi > 1970:
            myd_dic['1970+'] += 1
            continue
        if ysi > 1950:
            myd_dic['1950+'] += 1
            continue
        myd_dic['1950-'] += 1

    return myd_dic


if __name__ == '__main__':
    print 'its main'
    l_src_dir = './ml-latest-small/ml-latest-small/'
    ratings = pd.read_csv(l_src_dir + 'ratings.csv', header=0)
    movies = pd.read_csv(l_src_dir + 'movies.csv', header=0)

    print ratings.rating.size

    a = [1,2,3]
    print len(a), range(1, 3)

    # ab = np.zeros((2,3))
    # print ab, type(ab)

    # mv_year_divide(movies.title)
    # if type(123) is int:
    #     print 'ye'
    # count = 0
    # a = [[1, 2], [3, 4]]
    # b = [5, 6]
    # res = np.dot(a, b)
    # print res
    # print ret_y_mn()
    # print count


