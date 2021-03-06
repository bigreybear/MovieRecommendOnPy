import numpy as np
import pandas as pd
import re
import movieRecom
import sys
from scipy.sparse import coo_matrix


def insider_watcher(obj, ws=False):
    for row in dir(obj):
        print row
    print 'And Type is {}'.format(type(obj))
    if ws:
        print obj
    return 0


def dict_watcher(dic, limit=0):
    for key in dic:
        print key, dic[key]
        limit -= 1
        if limit == 0:
            break
    return 0


def ret_y_mn(mvn='Hl (aa) and (122) this a; (1923)'):
    patt = re.compile(u'\d{4}\D*$')
    res_re_p = re.search(patt, mvn)
    if not res_re_p:
        # print mvn
        # print 'match failed, and failed info is above'
        return 0
    patt2 = re.compile(u'\d*')
    resrep = re.search(patt2, res_re_p.group())
    return int(resrep.group())


def mv_year_divide(mvns):
    titles = mvns.values
    myd_dic = {'1950-': 0, '1950+': 0, '1970+': 0, '1990+': 0, '2006+': 0, '2011+':0}
    for ys in titles:
        ysi = ret_y_mn(ys)
        if ysi > 2011:
            myd_dic['2011+'] += 1
            continue
        if ysi > 2006:
            myd_dic['2006+'] += 1
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


def pre_vecs(va, vb):
    lg = len(va)
    lg_b = len(vb)
    n_c = 0
    nra = []
    nrb = []
    rat_uid = []
    if lg != lg_b:
        print 'There must be some mistake!'
        return 0
    for i in range(lg):
        # all val in vec should be calc-ed
        if type(va[i]) is not float:
            nra.append(va[i, 0])
            nrb.append(vb[i, 0])
        else:
            nra.append(va[i])
            nrb.append(vb[i])
        n_c += 1
    return nra, nrb, n_c, rat_uid


if __name__ == '__main__':
    print 'its main'
    l_src_dir = './ml-latest-small/ml-latest-small/'
    src_dir_20m = './ml-20m/ml-20m/'
    ratings = pd.read_csv(l_src_dir + 'ratings.csv', header=0)
    movies = pd.read_csv(l_src_dir + 'movies.csv', header=0)

    ar_1 = [0, 3.5, 5.0, 3.5, 0, 3.0, 5.0]
    ar_2 = [0, 3.0, 3.5, 0, 2.0, 2.0, 0]

    # print sorted(ar_1, reverse=True)
    #
    # ar_1.sort(reverse=True)
    #
    # print ar_1

    aaa = np.zeros([3,1])
    print aaa
    aaa[2,0] = 3
    print aaa

    """
    # Test matrix dot plus by numpy
    """
    # asc = np.zeros([4,7])
    # print asc
    # asc[3][5] = 2
    # asc[2][1] = 4
    # print asc
    # ascd = coo_matrix(asc)
    # asc = ascd.todense()
    # print asc
    # vec = np.zeros([7,1])
    # print vec
    # vec[1][0] = 1
    # print asc, vec
    # print np.dot(asc, vec)

    # ar_1, ar_2, _ = pre_vecs(ar_1, ar_2)
    # print ar_1
    # print ar_2
    # print movieRecom.pearson_coe(ar_1, ar_2)
    # print np.zeros([3,3])
    # print range(1,3)
    # print movieRecom.pearson_p34([2.,2.])

    # mvs_rat = [()] * 5
    # mvs_rat[2] = (12,3,6)
    # print mvs_rat

    # print ac
    # print b
    # b = a.tolist()
    # print a
    # print b, b.index(2)
    # print a
    # b = a * 2
    # print b
    # # print a + b
    # print 'hell'
    # print b[0, 1]
    #
    # c = np.arange(12).reshape(4,3)
    # print c, c[0][0], c[1][2]
    # ab = np.zeros((2,3))
    # print ab, type(ab)

    # res = mv_year_divide(movies.title)
    # dict_watcher(res)
    # if type(123) is int:
    #     print 'ye'
    # count = 0
    # a = [[1, 2], [3, 4]]
    # b = [5, 6]
    # res = np.dot(a, b)
    # print res
    # print ret_y_mn()
    # print count


