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
        self.limit_year = 1998
        self.movie_cnt = 0
        self.popular_mov = []
        self.classic_mov = []
        # related_mov and marked_mov is a np.matrix N*1
        self.related_mov = None
        self.marked_mov = None
        # know , like or hate, these need not to be present
        # cell of marked_mov_index is the index of marked mov
        self.marked_mov_index = []
        self.marked_cnt = 0
        # search_out and recommend_out is the content on the related lists
        self.search_out = []
        self.recommend_out = []
        # Note that it cant be rewrite !
        self.fac_ref = None
        self.prm_ref = None

    def movie_index_to_year(self, index):
        """
        Get year of the movie from its index swiftly
        :param index: movie index
        :return: movie year
        """
        return uutil.ret_y_mn(self.fac_ref['index_movieNm'][index])

    def mount(self, fac, prm=None):
        self.fac_ref = fac
        self.prm_ref = prm
        self.movie_cnt = fac['mvs_cnt']
        self.m_recom_list.InsertColumn(0, "title")
        self.m_recom_list.InsertColumn(1, "rates")
        self.m_recom_list.SetColumnWidth(0, 280)
        self.m_recom_list.SetColumnWidth(1, 50)

        self.marked_mov = np.zeros([fac['mvs_cnt'], 1])

        """
        # Next block is to init the recommend list
        """
        for i in range(fac['mvs_cnt']):
            pop_m = (i, fac['mvs_rat'][i][1])  # index and rate_cnt of a movie
            cla_m = (i, fac['mvs_rat'][i][0])  # index and rate of a movie
            self.popular_mov.append(pop_m)
            self.classic_mov.append(cla_m)
        self.popular_mov.sort(key=lambda j: self.movie_index_to_year(j[0]), reverse=True)
        self.popular_mov.sort(key=lambda k: k[1], reverse=True)
        self.classic_mov.sort(key=lambda k: self.movie_index_to_year(k[0]), reverse=True)
        self.classic_mov.sort(key=lambda k: k[1], reverse=True)

        """
        # temp test
        """
        # for i in range(200):
        #     # print self.popular_mov[i]
        #     print self.classic_mov[i], fac['index_movieNm'][self.classic_mov[i][0]]

        seed_a = random.randint(1, 30)
        seed_b = 30 - seed_a

        for i in range(self.movie_cnt):
            if self.movie_index_to_year(self.classic_mov[i][0]) <= self.limit_year:
                continue
            self.recommend_out.append(self.classic_mov[i][0])
            seed_b -= 1
            if seed_b == 0:
                break

        for i in range(self.movie_cnt):
            if self.movie_index_to_year(self.popular_mov[i][0]) <= self.limit_year:
                continue
            self.recommend_out.append(self.popular_mov[i][0])
            seed_a -= 1
            if seed_a == 0:
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
        self.check_out_list()
        self.write_search_list()


    def like_it(self, event):
        nms = self.m_recom_list.GetFirstSelected()
        m_ind =  self.recommend_out[nms]
        print nms
        if m_ind not in self.marked_mov_index:
            self.marked_mov_index.append(m_ind)
        self.marked_mov[m_ind, 0] = 4
        self.marked_cnt += 1
        self.rearrange_out_list()

    def hate_it(self, event):
        nms = self.m_recom_list.GetFirstSelected()
        m_ind =  self.recommend_out[nms]
        print nms
        if m_ind not in self.marked_mov_index:
            self.marked_mov_index.append(m_ind)
        self.marked_mov[m_ind, 0] = -0.5
        self.marked_cnt += 1
        self.rearrange_out_list()


    def thats_it(self, event):
        nms = self.m_search_list.GetSelection()
        # print nms, self.search_out[nms][0]
        self.marked_cnt += 1
        if self.search_out[nms][1] not in self.marked_mov_index:
            self.marked_mov_index.append(self.search_out[nms][1])
        self.marked_mov[self.search_out[nms][1], 0] = 5
        print self.marked_mov_index
        self.rearrange_out_list()


    def write_search_list(self):
        """
        A cell of the list is a tuple, (movie name, movie index)
        All cell in list will be output
        :return: 
        """
        del_cnt = self.m_search_list.GetCount()
        for i in range(del_cnt):
            self.m_search_list.Delete(0)

        for i in range(len(self.search_out)):
            self.m_search_list.Insert(self.search_out[i][0], self.m_search_list.GetCount())


    def write_recom_list(self):
        """
        A cell of list is a index of the movie
        All cell in list will be output
        """
        self.m_recom_list.DeleteAllItems()
        rd_list = self.recommend_out
        for i in range(len(rd_list)):
            self.m_recom_list.InsertStringItem(i, self.fac_ref['index_movieNm'][rd_list[i]])
            self.m_recom_list.SetStringItem(i, 1, str(self.fac_ref['mvs_rat'][rd_list[i]][0]))


    def rearrange_out_list(self):
        """
        Triggered by action marked, through button like_it, hate_it and that_it
        Notice that prm(Pearson Relation Matrix) doesn't include any movie early than self.from_year
        :return: 
        """
        unsort_rec_list = []

        del self.recommend_out
        self.recommend_out = []
        self.related_mov = np.dot(self.prm_ref, self.marked_mov)
        for i in range(self.movie_cnt):
            if self.related_mov[i, 0] > 0:
                # print i, self.related_mov[i, 0], self.fac_ref['index_movieNm'][i]
                if i not in self.marked_mov_index:
                    unsort_rec_list.append((i, self.related_mov[i, 0], self.movie_index_to_year(i)))
        # unsort_rec_list.sort(key=lambda k: k[2], reverse=True)
        unsort_rec_list.sort(key=lambda k: k[1], reverse=True)

        if self.marked_cnt > 5:
            """
            # Output is all depend on marked movies
            """
            for i in range(50):
                if i >= len(unsort_rec_list):
                    break
                if self.movie_index_to_year(unsort_rec_list[i][0]) > self.limit_year:
                    self.recommend_out.append(unsort_rec_list[i][0])
                print unsort_rec_list[i][1]
            pass

        elif self.marked_cnt > 0:
            """
            # Output is a remix
            """
            for i in range(50):
                if i%4 == 1:
                    self.recommend_out.append(self.popular_mov[i][0])
                elif i%4 == 2:
                    self.recommend_out.append(self.classic_mov[i][0])
                else:
                    if i >= len(unsort_rec_list):
                        break
                    if self.movie_index_to_year(unsort_rec_list[i][0]) > self.limit_year:
                        self.recommend_out.append(unsort_rec_list[i][0])
            pass
        else:
            """
            # Output is random
            """
            seeds = random.randint(1,3)
            for i in range(50):
                if i%seeds == 1:
                    self.recommend_out.append(self.popular_mov[i][0])
                else:
                    self.recommend_out.append(self.classic_mov[i][0])
            pass

        """
        # re-arrange search_out, check out_list
        """
        self.check_out_list()
        self.write_search_list()
        self.write_recom_list()
        pass

    def check_out_list(self):
        if self.recommend_out is not None:
            pass
        if self.search_out is not None:
            list_len = len(self.search_out)
            to_del = []
            for i in range(list_len):
                if self.search_out[i][1] in self.marked_mov_index:
                    to_del.append(i)
            for k in to_del:
                del (self.search_out[k])
            pass
        pass

    def want_more(self, event):
        """
        In fact, its a test function button
        Now to restart the recommendation
        :param event: 
        :return: 
        """
        del self.marked_mov
        del self.marked_mov_index
        self.marked_mov = np.zeros([self.movie_cnt, 1])
        self.marked_mov_index = []
        self.marked_cnt = 0
        self.rearrange_out_list()


if __name__ == "__main__":
    movieRecom.main()
