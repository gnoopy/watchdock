import sys
import wx
import os
import subprocess
import psutil
import time
import thread
import signal
from threading import *

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, cmd):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.cmd = cmd
        self.proc = None
        # self.start()

    def run(self):
        """Run Worker Thread."""

        self.proc = subprocess.Popen(self.cmd, shell=True,  
                        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        print
        while True:
            time.sleep(0.5)
            line = self.proc.stdout.readline()
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(self.proc.pid))
                return
            else:
                wx.SafeYield()
            
            if line.strip() == "":
                pass
            else:
                print line.strip()
            if not line and self.proc.poll() is not None: 
                break
        wx.PostEvent(self._notify_window, ResultEvent(None))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1


class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
 

class LogTailer(wx.Dialog):
 
    def __init__(self, cmd):
        wx.Dialog.__init__(self, None, wx.ID_ANY)
        self.cmd = cmd
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self,wx.ID_ANY)
        self.log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.btn = wx.Button(panel, ID_STOP, 'Quit')
        self.Bind(wx.EVT_BUTTON, self.OnPressedClose, self.btn, id=ID_STOP)
        self.Bind(wx.EVT_SHOW, self.OnShowDialog, self, id=ID_START)

        # Add widgets to a sizer        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn, 0, wx.ALL|wx.CENTER, 5)
        # self.btn.Disable()
        panel.SetSizer(sizer)
        
        # redirect text here
        self.redir=RedirectText(self.log)
        sys.stdout=self.redir


        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)

        # And indicate we don't have a worker thread yet
        self.worker = None

    def OnResult(self, event):
        """Show Result status."""
        if event.data is not None:
            p = psutil.Process(event.data)
            p.terminate()
            # os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 
            print("Process killed")
            # sys.stdout = sys.__stdout__
            self.EndModal(wx.ID_CANCEL)
        else:
            print("Process finished")
        self.worker = None
        print("OnResult:%s"%event.data)

    def OnShowDialog(self, event):
        print("OnShow Called..")
        if not self.worker:
            print('Starting thread ')
            self.worker = WorkerThread(self, self.cmd)
            self.worker.start()

    def OnPressedClose(self, event):
        # if self.proc.poll() is None: # A nagative value -N indicates that the child was terminated by signal N 
        if self.worker:
            print('Trying to abort')
            self.worker.abort()
        else:
            sys.stdout = sys.__stdout__
            self.EndModal(wx.ID_CANCEL)

