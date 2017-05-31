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
                # store a list of related info
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
        return 0


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



