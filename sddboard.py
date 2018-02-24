#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

import subprocess
import shlex
import threading
import time
from wx.lib.pubsub import pub
from threading import Thread
import wx.lib.agw.pyprogress as PP



class ProgressThread(Thread):
    """Test Worker Thread Class."""
 
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread

    def run(self):
        """Run Worker Thread."""
        wx.MilliSleep(100)
        pub.sendMessage("update", msg="")


class MyProgressDialog(wx.lib.agw.pyprogress.PyProgress):
    """"""
    def __init__(self,act_msg):
        """Constructor"""
        wx.lib.agw.pyprogress.PyProgress.__init__(self,None, -1, "Command Execution",
                            act_msg,                            
                            agwStyle=wx.PD_APP_MODAL )
        self.SetGaugeSteps(50)
        self.SetGaugeBackground(wx.WHITE)
        self.SetGaugeProportion(0.2)
        self.SetFirstGradientColour(wx.WHITE)
        self.SetSecondGradientColour(wx.GREEN)
        self.SetSize(300,self.GetSize()[1])

        self.stopNow = False
        # create a pubsub listener
        pub.subscribe(self.updateProgress, "update")
    
    def updateProgress(self, msg):
        """
        Update the progress bar
        """
        if msg == "-1" :
            self.stopNow=True
            wx.MilliSleep(50)
            self.Hide()
            self.Destroy()
            wx.SafeYield()
            wx.GetApp().GetTopWindow().Raise()
        else:
            keepGoing=True
            while keepGoing:
                wx.MilliSleep(30)
                if self.stopNow :
                    break;
                keepGoing = self.UpdatePulse()
       
        
    

class DockerDashBoard(wx.Frame):
    def __init__(self, parent, title):
        super(DockerDashBoard, self).__init__(parent, title=title,
                                              size=(1200, 600))
        self.count = 0
        self.InitUI()
        self.Centre()
        self.Show()
        # worker = TailingThread(self, 1)
        # worker.start()
    
    def InitUI(self):
        font1 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Monaco')

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # fgs = wx.FlexGridSizer(3, 2, 9, 25)
        fgs = wx.FlexGridSizer(4, 2, 0, 0)

        stats = wx.StaticText(panel, label="Commands")
        containers = wx.StaticText(panel, label="Containers")
        images = wx.StaticText(panel, label="Images")
        dockersys = wx.StaticText(panel, label="System")

        panel2 = wx.Panel(panel)
        box = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(panel2, style=wx.TE_MULTILINE)
        self.cmd_cont_info = self.run_cmd_sync('docker container ls -a')
        lines = self.cmd_cont_info.splitlines()
        self.lst = wx.ListBox(panel2, size=(100, -1),
                              choices=lines[1:], style=wx.LB_SINGLE)
        # lst = wx.ListBox(panel2, size = (100,-1), choices = [], style = wx.LB_SINGLE)

        lbl = wx.StaticText(panel2, size=(100, -1), label=lines[0])
        self.text.SetFont(font1)
        self.lst.SetFont(font1)
        lbl.SetFont(font1)
        box.Add(lbl, 0, wx.EXPAND)
        box.Add(self.lst, 1, wx.EXPAND)
        box.Add(self.text, 2, wx.EXPAND)
        panel2.SetSizer(box)
        panel2.Fit()
        panel.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst)

        # wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.tc1 = panel2
        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        action_panel = wx.Panel(panel)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_refresh = wx.Button(action_panel, -1, "refresh")
        self.btn_stop = wx.Button(action_panel, -1, "stop")
        self.btn_restart = wx.Button(action_panel, -1, "restart")
        self.btn_start = wx.Button(action_panel, -1, "start")

        self.btn_del = wx.Button(action_panel, -1, "delete")

        self.btn_stop.Disable()
        self.btn_restart.Disable()
        self.btn_start.Disable()
        self.btn_del.Disable()

        action_panel.SetSizer(hbox2)
        hbox2.AddSpacer(10)
        hbox2.Add(self.btn_refresh, 0, wx.ALIGN_CENTER)
        hbox2.AddSpacer(10)
        hbox2.Add(self.btn_stop, 0, wx.ALIGN_CENTER)
        hbox2.Add(self.btn_restart, 0, wx.ALIGN_CENTER)
        hbox2.Add(self.btn_start, 0, wx.ALIGN_CENTER)

        hbox2.AddSpacer(10)
        hbox2.Add(self.btn_del, 0, wx.ALIGN_CENTER)

        self.btn_refresh.Bind(wx.EVT_BUTTON, self.OnClickedRefresh)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.OnClickedStop)
        self.btn_restart.Bind(wx.EVT_BUTTON, self.OnClickedRestart)
        self.btn_start.Bind(wx.EVT_BUTTON, self.OnClickedStart)

        # self.tc4 = wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.tc1.SetFont(font1)
        self.tc2.SetFont(font1)
        self.tc3.SetFont(font1)
        action_panel.SetFont(font1)

        self.cmd_imgs_info = self.run_cmd_sync('docker images')
        self.cmd_df_info = self.run_cmd_sync('docker system df')
        self.tc2.SetValue(self.cmd_imgs_info)
        self.tc3.SetValue(self.cmd_df_info)
        # self.run_command('docker stats',tc4)

        fgs.AddMany([(stats), (action_panel, 1, wx.EXPAND), (containers), (self.tc1, 1, wx.EXPAND), (images),
                     # fgs.AddMany([(stats), (self.tc4, 1, wx.EXPAND), (images),
                     (self.tc2, 1, wx.EXPAND), (dockersys, 1, wx.EXPAND), (self.tc3, 1, wx.EXPAND)])
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableRow(3, 1)
        fgs.AddGrowableCol(1, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        panel.SetSizer(hbox)

    def OnClickedStop(self, event):
        ProgressThread()
        dlg=MyProgressDialog("Stopping container... ")
        threading.Thread(target=self.stop,args=[self.cont_id]).start()
        
    def OnClickedRestart(self, event):
        ProgressThread()
        dlg=MyProgressDialog("ReStarting container... ")
        threading.Thread(target=self.restart,args=[self.cont_id]).start()        
        # self.restart(self.cont_id)

    def OnClickedStart(self, event):
        ProgressThread()
        dlg=MyProgressDialog("Starting container... ")
        threading.Thread(target=self.start,args=[self.cont_id]).start()        
        # self.start(self.cont_id)

    def OnClickedRefresh(self, event):
        self.refresh()
        # btn = event.GetEventObject().GetLabel()
        # print "Label of pressed button = ", btn

    def stop(self, id):
        self.run_cmd_sync('docker container stop '+id)
        self.refresh()

    def restart(self, id):
        self.run_cmd_sync('docker container restart '+id)
        self.refresh()
    def start(self, id):
        self.run_cmd_sync('docker container start '+id)
        self.refresh()

    def refresh(self):
        self.cont_id=None
        sout = self.run_cmd_sync('docker container ls -a')
        if self.cmd_cont_info != sout:
            lines = sout.splitlines()
            self.lst.SetItems(lines[1:])

        sout = self.run_cmd_sync('docker images')
        if self.cmd_imgs_info != sout:
            self.tc2.SetValue(sout)

        sout = self.run_cmd_sync('docker system df')
        if self.cmd_df_info != sout:
            self.tc3.SetValue(sout)

        pub.sendMessage("update", msg="-1")
        # wx.CallAfter(pub.sendMessage, "update", msg="-1")

    def onListBox(self, event):
        container_line = event.GetEventObject().GetStringSelection()
        self.cont_id = container_line[0:12]
        top = self.run_cmd_sync('docker container top '+self.cont_id)+"----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        # logs=self.run_cmd_sync('docker container logs '+con_id+' --timestamps')
        logs = self.run_cmd_sync('docker container logs '+self.cont_id+'')
        self.text.SetValue(container_line+"\n"+top+logs)
        if "Up" in container_line and "Exited (" not in container_line:
            self.btn_stop.Enable()
            self.btn_restart.Enable()
        else:
            self.btn_stop.Disable()
            self.btn_restart.Disable()
            self.btn_start.Enable()

    def run_cmd_sync(self, command):
        process = subprocess.Popen(shlex.split(
            command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tup = process.communicate()
        stdout = tup[0]+tup[1]
        # print("tup--> "+str(tup))
        return stdout


if __name__ == '__main__':
    app = wx.App()
    frame = DockerDashBoard(None, title='Simple Docker Dashboard')
    app.MainLoop()
