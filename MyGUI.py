import numpy as np
import guiExample
import movieRecom


class TheFrame(guiExample.MyFrame1):
    def __del__(self):
        pass


class ThePanel(guiExample.MyPanel1):
    def __init__(self, parent):
        super(ThePanel, self).__init__(parent)
        self.fet = 5
        self.poplular_mov = []
        self.classic_mov = []
        self.related_mov = None
        self.marked_mov = None
        self.marked_cnt = 0
        self.search_out = []
        self.recommend_out = []
        # Note that it cant be rewrite !!!
        self.fac_ref = None

    def mount(self, fac):
        self.fac_ref = fac
        pass

    def search_pat(self, event):
        print 'its been son'
        print self.fet
        res = self.m_search_pat.GetValue()
        print res
        res = movieRecom.search_mov_name(self.fac_ref, res, 2006)
        print res

