# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 700),
                          style=wx.TAB_TRAVERSAL)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"select what you like or search for what you know",
                                           wx.DefaultPosition, wx.Size(-1, 15), 0)
        self.m_staticText4.Wrap(-1)
        bSizer5.Add(self.m_staticText4, 0, wx.ALL, 15)

        bSizer4.Add(bSizer5, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_search_pat = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(350, -1), 0)
        bSizer6.Add(self.m_search_pat, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_but_search = wx.Button(self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.Size(120, 35), 0)
        bSizer6.Add(self.m_but_search, 0, wx.ALIGN_CENTER | wx.ALL | wx.SHAPED, 5)

        bSizer4.Add(bSizer6, 1, 0, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        m_search_listChoices = []
        self.m_search_list = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, 150), m_search_listChoices, 0)
        bSizer9.Add(self.m_search_list, 0, wx.ALL, 5)

        self.m_but_know = wx.Button(self, wx.ID_ANY, u"That's it", wx.DefaultPosition, wx.Size(120, -1), 0)
        bSizer9.Add(self.m_but_know, 0, wx.ALL, 5)

        bSizer4.Add(bSizer9, 1, 0, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_recom_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, 375), wx.LC_ICON)
        bSizer7.Add(self.m_recom_list, 0, wx.ALL, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_but_like = wx.Button(self, wx.ID_ANY, u"I like it", wx.DefaultPosition, wx.Size(120, -1), 0)
        bSizer8.Add(self.m_but_like, 0, wx.ALL, 5)

        self.m_but_hate = wx.Button(self, wx.ID_ANY, u"I hate it", wx.Point(-1, -1), wx.Size(120, -1), 0)
        bSizer8.Add(self.m_but_hate, 0, wx.ALL, 5)

        self.m_but_more = wx.Button(self, wx.ID_ANY, u"I want more..", wx.DefaultPosition, wx.Size(120, -1), 0)
        bSizer8.Add(self.m_but_more, 0, wx.ALL, 5)

        bSizer7.Add(bSizer8, 1, 0, 5)

        bSizer4.Add(bSizer7, 1, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"Movie Seeker", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer10.Add(self.m_staticText5, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizer4.Add(bSizer10, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        # Connect Events
        self.m_but_search.Bind(wx.EVT_BUTTON, self.search_pat)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def search_pat(self, event):
        print 'it happened!'
        event.Skip()


