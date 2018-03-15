import wx
import wx.lib.busy as busy

class ContBusyInfo(busy.BusyInfo):
    def __init__(self, msg, parent=None, bgColour=None, fgColour=None):
        self.frame = _ContInfoFrame(parent, msg, bgColour, fgColour)
        self.frame.Show()
        self.frame.Refresh()
        self.frame.Update()

class _ContInfoFrame(wx.Frame):
    def __init__(self, parent, msg, bgColour=None, fgColour=None):
        wx.Frame.__init__(self, parent, style=wx.BORDER_SIMPLE|wx.FRAME_TOOL_WINDOW|wx.STAY_ON_TOP)

        bgColour = bgColour if bgColour is not None else wx.Colour(253, 255, 225)
        fgColour = fgColour if fgColour is not None else wx.BLACK

        panel = wx.Panel(self)
        text = StaticText(panel, -1, msg)
        text.SetForegroundColour(fgColour)
        
        for win in [panel, text]:
            win.SetCursor(wx.HOURGLASS_CURSOR)
            win.SetBackgroundColour(bgColour)
            win.SetForegroundColour(fgColour)
            
        size = text.GetBestSize()
        self.SetClientSize((size.width + 60, size.height + 40))
        panel.SetSize(self.GetClientSize())
        text.Center()
        self.Center()