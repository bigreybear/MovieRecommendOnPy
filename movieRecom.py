import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import sys
import uutil
import time
import math
from scipy.sparse import coo_matrix
try:
    import cPickle as pickle
except ImportError:
    import pickle


def check_rel_between(a, b, avgs, fcs):
    recs = []
    cell = {}
    sum_cnt = 0
    usrs_rats = fcs['usrs_rat']
    for key in usrs_rats:
        finds = 0
        for tups in usrs_rats[key]:
            if (tups[0] == a) or (tups[0] == b):
                if finds == 1:
                    cell['b'] = tups[1]
                    recs.append(cell)
                    cell = {}
                    finds = 0
                    pass
                elif finds == 0:
                    cell['a'] = tups[1]
                    cell['u'] = key
                    finds = 1
    for u in recs:
        average = avgs[u['u']+1][0]
        dis1 = u['a'] - average
        dis2 = u['b'] - average
        if (dis1 < 0) and (dis2 < 0):
            sum_cnt += 0
        else:
            rlr =dis1 * dis2
            sum_cnt += rlr
        print u, avgs[fcs['index_userId'][u['u']]], 'rlr:', rlr
    print 'expected repm:', sum_cnt


def construct_avg_rat(df_ur_rat, factor, mandatery_flash=False):
    # now it can handle 671 correctly
    # avg_rat is a list, key is the userId, and content is avg and cnt
    # avg_rat[0], avg_rat[-1] is for no use
    pio_str = 'hello world'
    if os.path.isfile('mid-data/avg_rat.dat') and not mandatery_flash:
        f = open('mid-data/avg_rat.dat', 'rb')

        avg_dat = pickle.load(f)

        print 'already a existing mid-data avg_rat'
        f.close()
        return avg_dat
    else:
        # usr_ind = factor['index_userId']
        print 'its a new mid-data avg_rat'
        f = open('mid-data/avg_rat.dat', 'wb')
        ###
        ###
        uid, rat = df_ur_rat.userId.values, df_ur_rat.rating.values
        cnt = df_ur_rat.userId.size
        print 'inside cnt:', cnt

        avg_rat = [0] * (factor['usr_cnt']+2)
        uid_n = uid[0]  # order of the userId
        rat_n = 0  # sum of rat during this user
        rat_cnt = 0  # count of rats during this user

        for index in range(0, cnt):
            if uid[index] == uid_n:
                rat_n += rat[index]
                rat_cnt += 1
            if (uid[index] != uid_n) or (index == cnt-1):
                # store a list of related info : avg_rat, rat_cnt
                # key is userId
                avg_rat[uid_n] = [round(1.*rat_n / rat_cnt, 2), rat_cnt]
                uid_n = uid[index]
                rat_n = rat[index]
                rat_cnt = 1

        pickle.dump(avg_rat, f)
        f.close()
        return avg_rat


def factor_builder(rat, mvs, mad_reb=False):
    print 'Start to build the factors, time:', time.strftime("%H:%M:%S")
    if os.path.isfile('mid-data/factors.dat') and not mad_reb:
        f = open('mid-data/factors.dat', 'rb')

        load_fb = pickle.load(f)
        load_fb['usr_rat_mat'] = load_fb['usr_rat_mat'].todense()
        print 'already a existing mid-data factors'
        f.close()
        print 'Factors loaded, time:', time.strftime("%H:%M:%S")
        return load_fb

    fb = {}

    mvs_cnt = mvs.movieId.unique().size
    fb['mvs_cnt'] = mvs_cnt

    # content is movieId
    # order is the index of movie (for matrix or csv)
    raws_m_m = mvs.movieId
    index_movieId = [0] * mvs_cnt
    index_movieNm = [''] * mvs_cnt
    movie_years = [0] *mvs_cnt
    for index in range(mvs_cnt):
        index_movieId[index] = raws_m_m[index]
        index_movieNm[index] = mvs.title[index]
        movie_years[index] = uutil.ret_y_mn(index_movieNm[index])
    fb['index_movieId'] = index_movieId
    fb['index_movieNm'] = index_movieNm
    fb['movie_years'] = movie_years

    usr_cnt = rat.userId.unique().size
    fb['usr_cnt'] = usr_cnt

    # content is userId
    # order is the index of user appeared in csv (for avg_rat)
    raws_m_m = rat.userId
    index_userId = [0] * usr_cnt
    e_index = 0
    index_userId[e_index] = raws_m_m[0]
    for index in range(len(raws_m_m)):
        if index_userId[e_index] != raws_m_m[index]:
            e_index += 1
            index_userId[e_index] = raws_m_m[index]
    fb['index_userId'] = index_userId

    usrs_rat = {}
    for index in range(len(rat.userId)):
        user_no = index_userId.index(rat.userId[index])
        if user_no not in usrs_rat:
            usrs_rat[user_no] = ((rat.movieId[index], rat.rating[index]), )
        else:
            usrs_rat[user_no] += ((rat.movieId[index], rat.rating[index]), )
    fb['usrs_rat'] = usrs_rat

    usr_rat_mat = np.zeros([usr_cnt, mvs_cnt])
    for key in usrs_rat:
        for tp in usrs_rat[key]:
            usr_rat_mat[key][index_movieId.index(tp[0])] = tp[1]
    fb['usr_rat_mat'] = usr_rat_mat

    sig_mv_rat = [0] * mvs_cnt
    sig_sqr_mr = [0] * mvs_cnt
    sig_coe = [0] * mvs_cnt
    for ind in range(mvs_cnt):
        for k in range(usr_cnt):
            sig_mv_rat[ind] = usr_rat_mat[k][ind]
            sig_sqr_mr[ind] = sig_mv_rat[ind] ** 2
        sig_coe[ind] = math.sqrt(sig_sqr_mr[ind] - sig_mv_rat[ind]*sig_mv_rat[ind]/usr_cnt)

    fb['sig_mv_rat'] = sig_mv_rat
    fb['sig_sqr_mr'] = sig_sqr_mr
    fb['sig_coe'] = sig_coe

    rat_cnt = rat.rating.size
    fb['rat_cnt'] = rat_cnt

    f = open('mid-data/factors.dat', 'wb')
    # notice that its been transformed to a sparse matrix
    fb['usr_rat_mat'] = coo_matrix(usr_rat_mat)
    pickle.dump(fb, f)
    f.close()
    fb['usr_rat_mat'] = fb['usr_rat_mat'].todense()
    print 'Factors built, time:', time.strftime("%H:%M:%S")
    return fb


def calc_repm_inc(cri, url, usrid):

    for index in range(len(url)):
        mv_na = url[index][0]
        rat_a = url[index][1]
        for i_ind in range(index+1, len(url)):
            mv_nb = url[i_ind][0]
            rat_b = url[i_ind][1]
            cri[mv_na][mv_nb] = round(rat_a * rat_b, 3)
            cri[mv_nb][mv_na] = round(rat_a * rat_b, 3)
            # print mv_na, mv_nb, rat_b*rat_a
            #
            # 6944 7526 8309
            if (mv_nb == 6944) and (mv_na == 7526):
                print rat_a, rat_b, cri[mv_nb][mv_na], usrid
            elif (mv_na == 6944) and (mv_nb == 7526):
                print rat_a, rat_b, cri[mv_nb][mv_na], usrid

    return cri


def represent_matrix_builder(rat, factor, dic_avg, mad_fla=False):
    print 'Start to build matrix, time:', time.strftime("%H:%M:%S")
    # rep-matrix already exist
    if os.path.isfile('mid-data/rep-matrix.dat') and not mad_fla:
        f = open('mid-data/rep-matrix.dat', 'rb')

        load_repm = pickle.load(f)

        print 'already a existing mid-data rep-matrix'
        f.close()
        print 'Matrix loaded, time:', time.strftime("%H:%M:%S")
        return load_repm

    # make a new matrix
    repm = np.zeros((factor['mvs_cnt'], factor['mvs_cnt']))
    repm_inc = np.zeros((factor['mvs_cnt'], factor['mvs_cnt']))
    pro_ing_uid = 0
    ready_to_merge = False
    ur_list = []
    ur_ind = factor['index_userId']
    for index in range(factor['rat_cnt']):
        # show the progress
        if index % 10000 == 0:
            print 'processed:', index
        if index > 100000:
            print index

        # rlr = (rat.rating[index] - dic_avg[rat.userId[index]][0])  # real like rate
        rlr = rat.rating[index]
        # print rlr
        # fill list of user-rat
        if pro_ing_uid != rat.userId[index]:
            # print ur_list
            # ready to calc the repm_inc, and calc it (calc_repm_inc)
            repm_inc = calc_repm_inc(repm_inc, ur_list, rat.userId[index])
            # abolish the old and create the new user-rat list
            ur_list = []
            pro_ing_uid = rat.userId[index]
            # fill the first tuple and ready to merge
            ready_to_merge = True

        # check if rat is valid for moive list, and filling the list anyway
        ur_list.append((factor['index_movieId'].index(rat.movieId[index]), rlr))

        # merge repm_inc and repm, clear the repm_inc
        if ready_to_merge:
            # 6944 7526 8309
            repm = repm_inc + repm
            if repm_inc[6944][7526] != 0:
                print 'In this addition', repm_inc[6944][7526], repm[6944][7526]
            repm_inc = np.zeros((factor['mvs_cnt'], factor['mvs_cnt']))
            ready_to_merge = False

        # test loops limit
        # if index>200:
        #     break

    # punish the hot item (not finished)
    # save the repm to the mid-date

    f = open('mid-data/rep-matrix.dat', 'wb')
    pickle.dump(repm, f)
    f.close()

    print 'Matrix calculated, time:', time.strftime("%H:%M:%S")
    return repm


def factory(src_dir):
    ratingReader = pd.read_csv(src_dir + 'ratings.csv', header=0)
    movieReader = pd.read_csv(src_dir + 'movies.csv')

    movieFreq = ratingReader.movieId.value_counts()
    print sys.getsizeof(2)
    #  print movieFreq.index
    #  print tryReadCsv

    #  print readMovie.loc[1:5]


def console_lookup(l_factors, l_rep_max):
    ins = 0
    while ins != 65535:
        ins = input("input the movieId you wang to learn. End by 65535:\n")
        t_ins = l_factors['index_movieId'].index(ins)
        res = l_rep_max[t_ins].tolist()
        b = []
        for i in range(len(res)):
            if res[i] > 25:
                b.append((res[i], i))
        cc = sorted(b, key=lambda bb: bb[0])
        print len(cc)
        for i in range(len(cc)):
            if res[i] != 0:
                print cc[i][0], factors['index_movieId'][cc[i][1]]


def pearson_p1(va, vb):
    nr = 0
    for i in range(len(va)):
        nr += va[i] * vb[i]
    return nr


def pearson_p2(va, vb, fac=None, ia=-1, ib=-1):
    if fac is None:
        localn = len(va)
        sig_a = 0
        sig_b = 0
        for i in range(localn):
            sig_a += va[i]
            sig_b += vb[i]
        ret = sig_b * sig_a
        ret = 1. * ret / localn
    else:
        ret = 1. * fac['sig_mv_rat'][ia] * fac['sig_mv_rat'][ib]
        ret = 1. * ret / fac['usr_cnt']
    return ret


def pearson_p12(va, vb, fac=None, ia=-1, ib=-1):
    return pearson_p1(va, vb) - pearson_p2(va, vb, fac, ia, ib)


def pearson_p34(vx, fac=None, ix=-1):
    sig_xs = 0
    sig_x = 0
    for i in range(len(vx)):
        sig_xs += vx[i] ** 2
        sig_x += vx[i]
    ret = sig_xs - sig_x*sig_x/len(vx)
    return ret


def pearson_p3456(va, vb, fac=None, ia=-1, ib=-1):
    if fac is None:
        ret = pearson_p34(va) * pearson_p34(vb)
        ret = math.sqrt(ret)
    else:
        ret = fac['sig_coe'][ia] * fac['sig_coe'][ib]
    return ret


def pearson_coe(va, vb, fac=None, ia=-1, ib=-1):
    va, vb, n, r_uid = uutil.pre_vecs(va, vb)
    if n == 0:
        return 0
    p12 = pearson_p12(va, vb)
    p3456 = pearson_p3456(va, vb, fac, ia, ib)
    # print p12, p3456

    if p3456 == 0:
        # print 'p3456 is zero'
        # print va
        # print vb
        return 0
    return p12 / p3456


def pearson_relate_matrix(fac, mad_reb=False, from_year=-1):
    print 'Start to build the pearson relate matrix, time:', time.strftime("%H:%M:%S")
    if os.path.isfile('mid-data/prm.dat') and not mad_reb:
        f = open('mid-data/prm.dat', 'rb')

        load_prm = pickle.load(f)
        load_prm = load_prm.todense()
        print 'already a existing mid-data prm'
        f.close()
        print 'Factors loaded, time:', time.strftime("%H:%M:%S")
        return load_prm

    # fac is for factors, all you need is in
    # below is how the matrix built
    urm = fac['usr_rat_mat']
    mvn = fac['mvs_cnt']
    prm = np.zeros([mvn, mvn])
    for o_index in range(mvn):
        # check year cons
        if fac['movie_years'][o_index] <= from_year:
            continue
        # report the progress
        if o_index % 1 == 0:
            print "Finished : ", o_index, "/", mvn
        vc_a = urm[:, o_index]
        for i_index in range(o_index+1, mvn):
            # check year cons
            if fac['movie_years'][i_index] <= from_year:
                continue

            if i_index % 1000 == 0:
                print "i_index : ", i_index, "/", mvn
            vc_b = urm[:, i_index]
            # the most hard part
            ress = pearson_coe(vc_a, vc_b)
            prm[o_index][i_index] = ress
            prm[i_index][o_index] = ress

    # above is the building process

    f = open('mid-data/prm-bt2011.dat', 'wb')
    # notice that its been transformed to a sparse matrix
    prm = coo_matrix(prm)
    pickle.dump(prm, f)
    f.close()
    print 'Pearson relate matrix built, time:', time.strftime("%H:%M:%S")
    return prm


if __name__ == '__main__':
    print 'its main'
    l_src_dir = './ml-latest-small/ml-latest-small/'
    ratings = pd.read_csv(l_src_dir + 'ratings.csv', header=0)
    movies = pd.read_csv(l_src_dir + 'movies.csv', header=0)

    factors = factor_builder(ratings, movies)

    # index_b = 9121
    # print time.strftime("%H:%M:%S")
    # for i in range(factors['mvs_cnt']):
    #     vsa = factors['usr_rat_mat'][:, i]
    #     vsb = factors['usr_rat_mat'][:, index_b]
    #     # print factors['usr_rat_mat'][441, 2]
    #     res = pearson_coe(vsa, vsb, factors, i, index_b)
    #     if i % 1000 == 0:
    #         print 'now at :', i
    #     if res>0.2:
    #         print res, i, factors['index_movieNm'][i], factors['movie_years'][i]
    # print time.strftime("%H:%M:%S")

    gm_prm = pearson_relate_matrix(factors, from_year=2011, mad_reb=True)
    # print gm_prm[9114, 9121], factors['index_movieNm'][9114]
    # print gm_prm[9121, 9114], factors['index_movieNm'][9121]
    #
    # # check for non-zero value and index
    # for oia in range(factors['mvs_cnt']):
    #     for oib in range(factors['mvs_cnt']):
    #         if gm_prm[oia, oib] != 0:
    #             print gm_prm[oia, oib]
    #             print oia, factors['index_movieNm'][oia]
    #             print oib, factors['index_movieNm'][oib]


    # check_rel_between(77561, 59315, avg, factors)

    # uutil.dict_watcher(factors['usrs_rat'], 10)
    # print factors['usrs_rat'][14]

    # iron man1:59315, 77561, 102125
    # 6944 7526 8309
    # print factors['index_movieId'].index(59315)
    # print factors['index_movieId'].index(77561)
    # print factors['index_movieId'].index(102125)
    # rep_max = represent_matrix_builder(ratings, factors, avg, True)
    # print rep_max[6944][7526]

    # console_lookup(factors, rep_max)


