import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import sys
import uutil
try:
    import cPickle as pickle
except ImportError:
    import pickle


def construct_avg_rat(df_ur_rat, mandatery_flash=False):
    pio_str = 'hello world'
    if os.path.isfile('mid-data/avg_rat.dat') and not mandatery_flash:
        f = open('mid-data/avg_rat.dat', 'rb')

        avg_dat = pickle.load(f)

        print 'already a existing mid-data avg_rat'
        f.close()
        return avg_dat
    else:
        print 'its a new mid-data avg_rat'
        f = open('mid-data/avg_rat.dat', 'wb')
        ###
        ###
        uid, rat = df_ur_rat.userId.values, df_ur_rat.rating.values
        cnt = df_ur_rat.userId.size
        print df_ur_rat.userId.index.min

        avg_rat = {}
        uid_n = 1
        rat_n = 0
        rat_cnt = 0

        for index in range(0, cnt):
            if uid[index] == uid_n:
                rat_n += rat[index]
                rat_cnt += 1

            else:
                # store a list of related info : avg_rat, rat_cnt
                avg_rat[uid_n] = [round(1.*rat_n / rat_cnt, 2), rat_cnt]
                uid_n = uid[index]
                rat_n = rat[index]
                rat_cnt = 1

        for row in avg_rat:
            print row, avg_rat[row]

        ###
        ###
        pickle.dump(avg_rat, f)
        f.close()
        return avg_rat


def factor_builder(rat, mvs):
    fb = {}


    mvs_cnt = mvs.movieId.unique().size
    fb['mvs_cnt'] = mvs_cnt

    # content is movieId
    # order is the index of movie (for matrix or csv)
    raws_m_m = mvs.movieId
    index_movieId = [0] * mvs_cnt
    for index in range(mvs_cnt):
        index_movieId[index] = raws_m_m[index]
    fb['index_movieId'] = index_movieId

    usr_cnt = rat.userId.unique().size
    fb['usr_cnt'] = usr_cnt

    rat_cnt = rat.rating.size
    fb['rat_cnt'] = rat_cnt
    return fb


def calc_repm_inc(cri, url):
    for index in range(len(url)):
        mv_na = url[index][0]
        rat_a = url[index][1]
        for i_ind in range(index+1, len(url)):
            mv_nb = url[i_ind][0]
            rat_b = url[i_ind][1]
            cri[mv_na][mv_nb] = round(rat_a * rat_b, 3)
            cri[mv_nb][mv_na] = round(rat_a * rat_b, 3)
            # print mv_na, mv_nb, rat_b*rat_a

    return cri


def represent_matrix_builder(rat, factor, dic_avg, mad_fla=False):
    # rep-matrix already exist
    if os.path.isfile('mid-data/rep-matrix.dat') and not mad_fla:
        f = open('mid-data/rep-matrix.dat', 'rb')

        load_repm = pickle.load(f)

        print 'already a existing mid-data rep-matrix'
        f.close()
        return load_repm

    # make a new matrix
    repm = np.zeros((factor['mvs_cnt'], factor['mvs_cnt']))
    repm_inc = np.zeros((factor['mvs_cnt'], factor['mvs_cnt']))
    pro_ing_uid = 0
    ready_to_merge = False
    ur_list = []
    for index in range(factor['rat_cnt']):
        # show the progress
        if index%100 == 0:
            print 'processed:', index

        # print rat.userId[index], rat.movieId[index], rat.rating[index],
        # print 'rating computed:',
        rlr = (rat.rating[index] - dic_avg[rat.userId[index]][0])  # real like rate
        # fill list of user-rat
        if pro_ing_uid != rat.userId[index]:
            # print ur_list
            # ready to calc the repm_inc, and calc it (calc_repm_inc)
            repm_inc = calc_repm_inc(repm_inc, ur_list)
            # abolish the old and create the new user-rat list
            ur_list = []
            pro_ing_uid = rat.userId[index]
            # fill the first tuple and ready to merge
            ready_to_merge = True

        # check if rat is valid for moive list, and filling the list anyway
        ur_list.append((factor['index_movieId'].index(rat.movieId[index]), rlr))

        # merge repm_inc and repm
        if ready_to_merge:
            repm = repm_inc + repm_inc
            ready_to_merge = False

        # test loops limit
        # if index>200:
        #     break

    # punish the hot item (not finished)
    # save the repm to the mid-date

    f = open('mid-data/rep-matrix.dat', 'wb')
    pickle.dump(repm, f)
    f.close()

    return repm



def factory(src_dir):
    ratingReader = pd.read_csv(src_dir + 'ratings.csv', header=0)
    movieReader = pd.read_csv(src_dir + 'movies.csv')

    movieFreq = ratingReader.movieId.value_counts()
    print sys.getsizeof(2)
    #  print movieFreq.index
    #  print tryReadCsv

    #  print readMovie.loc[1:5]


if __name__ == '__main__':
    print 'its main'
    l_src_dir = './ml-latest-small/ml-latest-small/'
    ratings = pd.read_csv(l_src_dir + 'ratings.csv', header=0)
    movies = pd.read_csv(l_src_dir + 'movies.csv', header=0)

    avg = construct_avg_rat(ratings)
    factors = factor_builder(ratings, movies)
    represent_matrix_builder(ratings, factors, avg)



