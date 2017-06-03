import wx
import MyGUI

def first_gui():
    app = wx.App()
    window = wx.Frame(None, title="wxPython", size=(400, 300))
    panel = wx.Panel(window)
    label = wx.StaticText(panel, label="Hello World", pos=(100, 100))
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    print 'its main gui'
    app = wx.App(False)
    frame = MyGUI.TheFrame(None)
    panel = MyGUI.ThePanel(frame)

    frame.Show()
    print 'arrived'
    app.MainLoop()

