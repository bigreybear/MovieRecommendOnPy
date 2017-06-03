import numpy as np
import guiExample
import movieRecom
import random
import uutil


class TheFrame(guiExample.MyFrame1):
    def __del__(self):
        pass


class ThePanel(guiExample.MyPanel1):
    def __init__(self, parent):
        super(ThePanel, self).__init__(parent)
        self.limit_year = 2006
        self.movie_cnt = 0
        self.popular_mov = []
        self.classic_mov = []
        self.related_mov = None
        self.marked_mov = None
        # know , like or hate, these need not to be present
        self.marked_mov_index = []
        self.marked_cnt = 0
        # search_out and recommend_out is the content on the related lists
        self.search_out = []
        self.recommend_out = []
        # Note that it cant be rewrite !
        self.fac_ref = None

    def movie_index_to_year(self, index):
        """
        Get year of the movie from its index swiftly
        :param index: movie index
        :return: movie year
        """
        return uutil.ret_y_mn(self.fac_ref['index_movieNm'][index])

    def mount(self, fac):
        self.fac_ref = fac
        self.movie_cnt = fac['mvs_cnt']
        self.m_recom_list.InsertColumn(0, "title")
        self.m_recom_list.InsertColumn(1, "rates")
        self.m_recom_list.SetColumnWidth(0, 300)
        self.m_recom_list.SetColumnWidth(1, 50)

        self.marked_mov = np.zeros([fac['mvs_cnt'], 1])

        """
        # Next block is to init the recommend list
        """
        for i in range(fac['mvs_cnt']):
            pop_m = (i, fac['mvs_rat'][1])  # index and rate_cnt of a movie
            cla_m = (i, fac['mvs_rat'][0])  # index and rate of a movie
            self.popular_mov.append(pop_m)
            self.classic_mov.append(cla_m)
        self.popular_mov.sort(key=lambda k:k[1], reverse=True)
        self.classic_mov.sort(key=lambda k:k[1], reverse=True)

        seed_a = random.randint(1, 30)
        seed_b = 30 - seed_a
        for i in range(self.movie_cnt):
            if self.movie_index_to_year(self.popular_mov[i][0]) < self.limit_year:
                continue
            self.recommend_out.append(self.popular_mov[i][0])
            seed_a -= 1
            if seed_a == 0:
                break
        for i in range(self.movie_cnt):
            if self.movie_index_to_year(self.classic_mov[i][0]) < self.limit_year:
                continue
            self.recommend_out.append(self.classic_mov[i][0])
            seed_b -= 1
            if seed_b == 0:
                break
        self.write_recom_list()
        pass

    def search_pat(self, event):
        print 'its been son'
        del_cnt = self.m_search_list.GetCount()
        for i in range(del_cnt):
            self.m_search_list.Delete(0)

        res = self.m_search_pat.GetValue()

        self.search_out = movieRecom.search_mov_name(self.fac_ref, res, self.limit_year)

        for i in range(len(self.search_out)):
            self.m_search_list.Insert(self.search_out[i][0], i)
            self.m_recom_list.InsertStringItem(i, self.search_out[i][0])
            self.m_recom_list.SetStringItem(i, 1, str(self.search_out[i][1]))


    def thats_it(self, event):
        nms = self.m_search_list.GetSelection()
        print nms
        self.write_recom_list()

    def write_search_list(self):
        del_cnt = self.m_search_list.GetCount()
        for i in range(del_cnt):
            self.m_search_list.Delete(0)

        for i in range(len(self.search_out)):
            if self.search_out[i][1] in self.marked_mov_index:
                continue
            self.m_search_list.Insert(self.search_out[i][0], i)

    def write_recom_list(self):
        """
        # a cell of list is a index of the movie
        """
        self.m_recom_list.DeleteAllItems()
        rd_list = self.recommend_out
        for i in range(len(rd_list)):

            self.m_recom_list.InsertStringItem(i, self.fac_ref['index_movieNm'][rd_list[i]])
            self.m_recom_list.SetStringItem(i, 1, str(self.fac_ref['mvs_rat'][i][0]))
