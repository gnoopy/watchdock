#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.0b3 on Thu Mar  8 01:09:42 2018
#

import sys,os
print sys.executable
print "\n".join(sys.path)

import wx
import wx.lib.busy as busy

    import terminal
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

import subprocess
import shlex
import threading
import time
from wx.lib.pubsub import pub
from threading import Thread
import wx.lib.agw.pyprogress as PP
import re
import platform
import cPickle
import coverage




class WatchdockFrame(wx.Frame):

    def __init__(self, parent, testing, id, **args):
        self.testing = testing
        self.mockdata = {}

        # self.testing = False
        self.font_name = "Menlo"
        if "Darwin" in platform.platform():
            self.font_name = "Monaco"
        elif "Ubuntu" in platform.platform():
            self.font_name = "Monospace"
        elif "Windows" in platform.platform():
            self.font_name = "Menlo"
        self.vmids=[]
        self.cmd_cont_info=""
        self.cmd_imgs_info =""
        self.cmd_df_info=""
        self.cmDlg = CommitDialog(" "," ")
        # kwds={}
        # args=()
        # begin wxGlade: WatchdockFrame.__init__
        # kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR
        default=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR
        wx.Frame.__init__(self, parent, style=default)
        # wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1024, 840))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.chc_vgt_ids = wx.Choice(self.panel_1, wx.ID_ANY, choices=["Host"])
        self.btn_refresh = wx.Button(self.panel_1, wx.ID_ANY, "refresh")
        self.btn_stop = wx.Button(self.panel_1, wx.ID_ANY, "stop")
        self.btn_restart = wx.Button(self.panel_1, wx.ID_ANY, "restart")
        self.btn_start = wx.Button(self.panel_1, wx.ID_ANY, "start")
        self.btn_save = wx.Button(self.panel_1, wx.ID_ANY, "save...")
        self.btn_push = wx.Button(self.panel_1, wx.ID_ANY, "push")
        self.btn_del = wx.Button(self.panel_1, wx.ID_ANY, "delete")
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_LIVE_UPDATE)
        self.pnl_container = wx.Panel(self.window_1, wx.ID_ANY)
        self.lbl_cont_header = wx.StaticText(self.pnl_container, wx.ID_ANY, "Waiting for docker container  information...")
        self.window_2 = wx.SplitterWindow(self.pnl_container, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_LIVE_UPDATE)
        self.lst_containers = wx.ListBox(self.window_2, wx.ID_ANY, choices=[])
        self.txt_details = wx.TextCtrl(self.window_2, wx.ID_ANY, "\n\n\n", style=wx.TE_DONTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.pnl_images = wx.Panel(self.window_1, wx.ID_ANY)
        self.window_3 = wx.SplitterWindow(self.pnl_images, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_LIVE_UPDATE)
        self.pnl_img = wx.Panel(self.window_3, wx.ID_ANY)
        self.lbl_img_header = wx.StaticText(self.pnl_img, wx.ID_ANY, "Waiting for docker image information...")
        self.lst_images = wx.ListBox(self.pnl_img, wx.ID_ANY, choices=[])
        self.pnl_imghst = wx.Panel(self.window_3, wx.ID_ANY)
        self.lbl_images_hst = wx.StaticText(self.pnl_imghst, wx.ID_ANY, "")
        self.lst_images_hst = wx.ListBox(self.pnl_imghst, wx.ID_ANY, choices=[])
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.txt_system = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.chc_vgt_ids)
        self.Bind(wx.EVT_BUTTON, self.OnClickedRefresh, self.btn_refresh)
        self.Bind(wx.EVT_BUTTON, self.OnClickedStop, self.btn_stop)
        self.Bind(wx.EVT_BUTTON, self.OnClickedRestart, self.btn_restart)
        self.Bind(wx.EVT_BUTTON, self.OnClickedStart, self.btn_start)
        self.Bind(wx.EVT_BUTTON, self.OnClickedSave, self.btn_save)
        self.Bind(wx.EVT_BUTTON, self.OnClickedPush, self.btn_push)
        self.Bind(wx.EVT_BUTTON, self.OnclickedDelete, self.btn_del)
        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst_containers)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDclickedContListBox, self.lst_containers)
        self.Bind(wx.EVT_LISTBOX, self.onImgListBox, self.lst_images)
        self.Bind(wx.EVT_LISTBOX, self.onImgHistBox, self.lst_images_hst)
        # end wxGlade
        if self.testing:
            f = open('./tests/mockdata.pkl','rb')
            self.mockdata=cPickle.load(f)
            self.panel_1.SetBackgroundColour(wx.YELLOW)
            self.refresh()
        else:
            wx.CallAfter(self.refresh)


    def __set_properties(self):
        # begin wxGlade: WatchdockFrame.__set_properties
        self.SetTitle("Watchdock")
        _icon = wx.NullIcon 
        _icon.CopyFromBitmap(wx.Bitmap("./watchdock/logo.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, self.font_name))
        self.chc_vgt_ids.SetMinSize((80, 23))
        self.chc_vgt_ids.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.chc_vgt_ids.SetToolTipString("Select vagrant vm ID")
        self.chc_vgt_ids.SetSelection(0)
        self.btn_refresh.SetMinSize((60, -1))
        self.btn_refresh.SetToolTipString("update all information from docker")
        self.btn_stop.SetMinSize((60, -1))
        self.btn_stop.SetToolTipString("Stop selected container")
        self.btn_stop.Enable(False)
        self.btn_restart.SetMinSize((60, -1))
        self.btn_restart.SetToolTipString("Restart selected container")
        self.btn_restart.Enable(False)
        self.btn_start.SetMinSize((60, -1))
        self.btn_start.SetToolTipString("Start selected container or image")
        self.btn_start.Enable(False)
        self.btn_save.SetMinSize((60, -1))
        self.btn_save.SetToolTipString("commit selected container \nto default image or other image")
        self.btn_save.Enable(False)
        self.btn_push.SetMinSize((60, -1))
        self.btn_push.SetToolTipString("Push saved image to docker cloud")
        self.btn_push.Enable(False)
        self.btn_del.SetMinSize((60, -1))
        self.btn_del.SetToolTipString("Delete selected image")
        self.btn_del.Enable(False)
        self.lbl_cont_header.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.lst_containers.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.txt_details.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.window_2.SetMinimumPaneSize(20)
        self.pnl_container.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.lbl_img_header.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.lst_images.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.lbl_images_hst.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.lst_images_hst.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.window_3.SetMinimumPaneSize(20)
        self.pnl_images.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.window_1.SetMinimumPaneSize(20)
        self.txt_system.SetMinSize((200, 120))
        self.txt_system.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: WatchdockFrame.__do_layout
        sizer_4 = wx.FlexGridSizer(3, 1, 0, 0)
        self.sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.panel_2, wx.ID_ANY, "System"), wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.pnl_images, wx.ID_ANY, "Images"), wx.VERTICAL)
        self.sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.pnl_container, wx.ID_ANY, "Containers"), wx.VERTICAL)
        self.sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Commands"), wx.HORIZONTAL)
        self.sizer_5.Add(self.chc_vgt_ids, 0, 0, 0)
        self.sizer_5.Add((10, 20), 0, 0, 0)
        self.sizer_5.Add(self.btn_refresh, 0, wx.ALL, 1)
        self.sizer_5.Add((10, 18), 0, 0, 0)
        self.sizer_5.Add(self.btn_stop, 0, wx.ALL, 1)
        self.sizer_5.Add(self.btn_restart, 0, wx.ALL, 1)
        self.sizer_5.Add(self.btn_start, 0, wx.ALL, 1)
        self.sizer_5.Add((10, 20), 0, 0, 0)
        self.sizer_5.Add(self.btn_save, 0, wx.ALL, 1)
        self.sizer_5.Add(self.btn_push, 0, wx.ALL, 1)
        self.sizer_5.Add(self.btn_del, 0, wx.ALL, 1)
        self.sizer_5.Add((0, 0), 0, 0, 0)
        self.sizer_5.Add((0, 0), 0, 0, 0)
        self.sizer_5.Add((0, 0), 0, 0, 0)
        self.sizer_5.Add((0, 0), 0, 0, 0)
        self.panel_1.SetSizer(self.sizer_5)
        sizer_4.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_8.Add(self.lbl_cont_header, 0, wx.EXPAND, 0)
        self.window_2.SplitHorizontally(self.lst_containers, self.txt_details)
        sizer_8.Add(self.window_2, 1, wx.EXPAND, 0)
        self.pnl_container.SetSizer(sizer_8)
        sizer_1.Add(self.lbl_img_header, 0, 0, 0)
        sizer_1.Add(self.lst_images, 1, wx.EXPAND, 0)
        self.pnl_img.SetSizer(sizer_1)
        self.sizer_2.Add(self.lbl_images_hst, 0, 0, 0)
        self.sizer_2.Add(self.lst_images_hst, 1, wx.EXPAND, 0)
        self.pnl_imghst.SetSizer(self.sizer_2)
        self.window_3.SplitVertically(self.pnl_img, self.pnl_imghst)
        sizer_7.Add(self.window_3, 1, wx.EXPAND, 0)
        self.pnl_images.SetSizer(sizer_7)
        self.window_1.SplitHorizontally(self.pnl_container, self.pnl_images)
        sizer_4.Add(self.window_1, 1, wx.EXPAND, 0)
        lbl_dockersys = wx.StaticText(self.panel_2, wx.ID_ANY, "Waiting for docker system  information...")
        lbl_dockersys.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, self.font_name))
        self.sizer_6.Add(lbl_dockersys, 0, wx.EXPAND, 0)
        self.sizer_6.Add(self.txt_system, 1, wx.EXPAND, 0)
        self.panel_2.SetSizer(self.sizer_6)
        sizer_4.Add(self.panel_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_4)
        sizer_4.AddGrowableRow(1)
        sizer_4.AddGrowableCol(0)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnChoice(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        #Add vagrant docker commands https://www.vagrantup.com/docs/cli/ssh.html
        with busy.BusyInfo("Receiving vagrant docker information... ",bgColour=wx.Colour(118,113,113)):
            wx.SafeYield() 
            self.refresh()

    def OnClickedRefresh(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        self.refresh()

    def OnClickedStop(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        with busy.BusyInfo("Stopping container... ", bgColour=wx.Colour(118,113,113)):
            wx.SafeYield()
            self.stop(self.cont_id)
        # threading.Thread(target=self.stop, args=[self.cont_id]).start()

    def OnClickedRestart(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        # if self.testing:
        #     self.restart(self.cont_id)            
        #     return
        with busy.BusyInfo("ReStarting container... ",bgColour=wx.Colour(118,113,113)):
            wx.SafeYield()
            self.restart(self.cont_id)

    def OnClickedStart(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        with busy.BusyInfo("Starting container... ",bgColour=wx.Colour(118,113,113)):
            wx.SafeYield() 
            self.start(self.cont_id)

    #76e0ceb7e72f        1and1internet/ubuntu-16:latest                 "/bin/bash -e /init/…"   37 hours ago        Up 37 hours                                                    ubuntu-16
    def get_imgtag_in_continfo(self, cont_line):
        # img_tag = cont_line[20:57].strip()
        m = re.search(r'(\S+)\s{2,}(\S+)\s{2,}', cont_line, re.M | re.I)
        img_tag = m.group(2)
        return img_tag

    def OnClickedSave(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        result=-1
        img_tag = self.get_imgtag_in_continfo(self.container_line) #[20:57].strip()
        self.cmDlg.SetRepository(self.cont_id,img_tag)
        self.cmDlg.CenterOnParent()
        
        result = self.cmDlg.ShowModal()
        if result == wx.ID_OK:
            msg = self.cmDlg.GetMsgValue()
            name = self.cmDlg.GetNameValue()
            imgtag = self.cmDlg.GetTagValue()
            self.cmDlg.Hide()
            self.cmDlg.Destroy()
            cmd = 'docker container commit -a "%s" -m "%s" %s %s'%(name, msg, self.cont_id, imgtag)
            # print('commit cmd ================================>',cmd)
            with busy.BusyInfo("Committing the container '%s' to the image '%s' ..."%(self.cont_id, imgtag), bgColour=wx.Colour(118,113,113)):
                wx.SafeYield() 
                self.run_cmd_sync(cmd)
            if self.testing:
                return
            self.refresh()
        else:
            print('You canceled')
            self.cmDlg.Destroy()

    def OnClickedPush(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        cmd = 'docker push %s'%(self.img_tag)
        # print cmd
        terminal_dlg = terminal.LogTailer(cmd)
        terminal_dlg.ShowModal()
        # terminal_dlg.Destroy()

    def OnclickedDelete(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        with busy.BusyInfo("Deleting image... ",bgColour=wx.Colour(118,113,113)):
            wx.SafeYield() 
            self.run_cmd_sync('docker image rm '+self.img_id)
        self.btn_del.Disable()
        if self.testing: #to prevent from getting dirty self.last_cmd_out due to refresh()
            return
        wx.CallAfter(self.refresh)
        # self.refresh()

    def onListBox(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        self.container_line = event.GetEventObject().GetStringSelection()
        self.cont_id = self.get_cont_id()
        top = self.run_cmd_sync('docker container top '+self.cont_id)+"\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        logs = self.run_cmd_sync('docker container logs '+self.cont_id+'')
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        logs = ansi_escape.sub('', logs)
        self.txt_details.SetValue(self.container_line+"\n"+top+logs)
        # if not self.testing :
        self.btn_push.Disable()
        if "Up" in self.container_line and "Exited (" not in self.container_line:
            self.btn_stop.Enable()
            self.btn_restart.Enable()
            self.btn_start.Disable()
            self.btn_save.Enable()
        else:
            self.btn_stop.Disable()
            self.btn_restart.Disable()
            self.btn_start.Enable()
            self.btn_save.Disable()

    def get_cont_id(self):
        return self.container_line[0:12] #0:12

    def get_cont_name(self):
        m=re.search( r'(\S+)\s{2,}(\S+)\s{2,}(\S+)\s{2,}', self.container_line, re.M|re.I)
        nm=m.group(3)
        return nm

    def OnDclickedContListBox(self, event):
        self.container_line = event.GetEventObject().GetStringSelection()
        self.cont_id = self.get_cont_id()
        self.cont_nm = self.get_cont_name()
        vgrnt_id=''
        if "Up" in self.container_line and "Exited (" not in self.container_line:
            sh_type="sh"
            sout=self.run_cmd_sync('docker exec -it %s ls /bin/bash'%self.cont_nm)
            # print("sout",sout)
            if "No such file" not in sout:
                sh_type=sout.strip()
            if len(self.vmids) >= 2 and self.chc_vgt_ids.GetSelection() > 0:
                tmp_index = self.chc_vgt_ids.GetSelection()
                vgrnt_id = self.chc_vgt_ids.GetString(tmp_index)
            #     docker_cmd= self.run_cmd_sync('vagrant ssh -c "which docker"').strip()
            # else: 
                # docker_cmd= self.run_cmd_sync('vagrant ssh -c "which docker"').strip()
            termscript="watchdock/term.bash "
            if "Windows" in platform.platform():
                termscript="watchdock/term.cmd "
            wx.CallAfter(self.run_cmd_sync, termscript+self.cont_nm+" "+sh_type+" "+vgrnt_id)

    def onImgListBox(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        img_line = event.GetEventObject().GetStringSelection()
        # self.img_id = img_line[58:71] #TODO: blank as separator should be considered
        self.img_id=self.get_img_id(img_line)
        self.img_tag=self.get_img_tag(img_line)
        str_history = self.run_cmd_sync('docker image history '+self.img_id+'')
        if str_history is not None:
            lines = str_history.splitlines()
            self.lbl_images_hst.SetLabel(lines[0])
            self.lst_images_hst.SetItems(lines[1:])
        if not self.testing:
            self.btn_del.Enable()
            if self.img_tag == "<none>":
                self.btn_push.Disable()
            else:
                self.btn_push.Enable()

    def onImgHistBox(self, event):  # wxGlade: WatchdockFrame.<event_handler>
        print("Event handler 'onImgHistBox' not implemented!")
        event.Skip()

    def wrap_vagrant_cmd(self,cmd_str):
        if len(self.vmids) >= 2 and self.chc_vgt_ids.GetSelection() > 0: #if vagrant id is selected rather than 'Host'
            cmd_str = 'vagrant ssh -c "'+cmd_str+'" '+self.chc_vgt_ids.GetStringSelection()
        return cmd_str

    def run_cmd_sync(self, command):
        if not command.strip().startswith("vagrant") and "term.bash"  not in command.strip():
            command = self.wrap_vagrant_cmd(command)
            # command.replace("-c","")
        stdout = ""
        print("command **********",command)
        if self.testing and command in self.mockdata.keys():
            stdout = self.mockdata[command]
        elif self.testing and command+"\r" in self.mockdata.keys():
            stdout = self.mockdata[command+"\r"]
        else:
            if self.testing:
                if "Windows" in platform.platform():
                    command="tests\\\\dummy.cmd " +command
                else:
                    command="tests/dummyshell "+command
            print("command2 **********",command)
  
            try:
                s=shlex.split(command.encode('ascii','ignore'))
                print('s',s)
                process = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                tup = process.communicate()
                stdout = tup[0]+tup[1]
            except Exception as e:
                print(os.getcwd())
                raise e
        if command.strip().startswith("vagrant"): #wrapped command
            regex = r'Connection to [0-9\.].* closed\.\s'
            stdout = re.sub(regex,'', stdout,0)
        ret = stdout.replace("\r","")

        # temporal use for test data record
        # f = open('./tests/mockdata.pkl','rb')
        # testdata = cPickle.load(f)
        # testdata[command]=ret
        # f = open('./tests/mockdata.pkl','wb')
        # cPickle.dump(testdata,f)
        # f.close()

        self.last_cmd_out=ret
        # print("---------------------------------------------------")
        # if self.testing and command not in self.mockdata.keys():
        #     print(command,"====>",self.last_cmd_out, "ret",ret)
        # print("---------------------------------------------------")
        return ret

    def get_img_id(self, img_line):
        # self.img_id = img_line[46:58]
        # print("img line :"+str(img_line)+"-----------------")
        m=re.search( r'(\S+)\s{2,}(\S+)\s{2,}(\S+)\s{2,}([0-9]+ [a-zA-Z]+ [a-zA-Z]+)\s{2,}(\S+)', img_line, re.M|re.I)
        img_id=m.group(3)
        # print("img id :"+str(img_id)+"-----------------")
        return img_id
    
    def get_img_tag(self, img_line):
        # print("img line :"+str(img_line)+"-----------------")
        m=re.search( r'(\S+)\s{2,}(\S+)\s{2,}(\S+)\s{2,}([0-9]+ [a-zA-Z]+ [a-zA-Z]+)\s{2,}(\S+)', img_line, re.M|re.I)
        img_tag=m.group(1)
        # print("img tag :"+str(img_tag)+"-----------------")
        return img_tag
    
    def get_vagrant_vmids(self):
        sout = self.run_cmd_sync("vagrant global-status")
        # print("get_vagrant_vmids",sout)
        ids = ['Host']
        if " no active Vagrant environments" in sout or sout is "":
            return ids
        else:
            lines = sout.splitlines()
            for line in lines[2:]:
                if "running" in line:
                    ids.append(line[0:7])
            return ids

    def get_img_history_str(self, id):
        str_history = self.run_cmd_sync('docker image history '+self.img_id+'')
        # lines = str_history.splitlines()
        return str_history

    def stop(self, id):
        self.run_cmd_sync('docker container stop '+self.cont_id)
        if self.testing: #to prevent from getting dirty self.last_cmd_out due to refresh()
            return
        wx.CallAfter(self.refresh)
        # self.refresh()

    def restart(self, id):
        self.run_cmd_sync('docker container restart '+self.cont_id)
        if self.testing: #to prevent from getting dirty self.last_cmd_out due to refresh()
            return
        wx.CallAfter(self.refresh)
        # self.refresh()

    def start(self, id):
        self.run_cmd_sync('docker container start '+self.cont_id)
        if self.testing: #to prevent from getting dirty self.last_cmd_out due to refresh()
            return
        wx.CallAfter(self.refresh)
        # self.refresh()

    def refresh(self):
        with wx.BusyCursor(cursor=wx.StockCursor(wx.CURSOR_WAIT)):
            tmp_index = self.chc_vgt_ids.GetSelection()
            old_vmid_str = self.chc_vgt_ids.GetString(tmp_index)
            self.vmids = self.get_vagrant_vmids()
            # print("old_vmid_str",old_vmid_str," ===>", "vmids",self.vmids )
            self.chc_vgt_ids.SetItems(self.vmids)
            sel = self.chc_vgt_ids.FindString(old_vmid_str)
            self.chc_vgt_ids.SetSelection(sel)
# docker container ls --format 'table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Ports}}\t{{.Mounts}}\t{{.Networks}}\t{{.RunningFor}}\t{{.Status}}\t{{.Size}}'
# docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}' 
            self.cont_id = None
            sout = self.run_cmd_sync("docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}'")
            if "Cannot connect to the Docker daemon" in sout or " the docker daemon is not running"  in sout:
                dlg = wx.MessageDialog(parent=None, message="Please run the docker service before run Simple Docker Dashboard"
                , caption="Error", style=wx.OK|wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
                # exit()
            if self.cmd_cont_info != sout:
                lines = sout.splitlines()
                self.lbl_cont_header.SetLabel(lines[0])
                self.lst_containers.SetItems(lines[1:])
                self.txt_details.Clear()
                self.btn_start.Disable()
                self.btn_restart.Disable()
                self.btn_stop.Disable()
                self.cmd_cont_info=sout
            sout = self.run_cmd_sync('docker images')
            if self.cmd_imgs_info != sout:
                self.cmd_imgs_info=sout
                lines = sout.splitlines()
                self.lbl_img_header.SetLabel(lines[0])
                self.lst_images.SetItems(lines[1:])
                # self.lst_images.SetSelection(0)
                if self.lst_images.GetSelection() is not wx.NOT_FOUND:
                    imgid=self.get_img_id(self.lst_images.GetStringSelection())
                    sout=self.get_img_history_str(imgid)
                    lines = sout.splitlines()
                    self.lst_images_hst.SetItems(lines[1:])
                else:
                    self.lst_images_hst.SetItems([])
                self.btn_del.Disable()

            sout = self.run_cmd_sync('docker system df')
            if self.cmd_df_info != sout:
                self.txt_system.SetValue(sout)
                self.cmd_df_info=sout

            pub.sendMessage("update", msg="-1")
        # del wait
        # wx.CallAfter(pub.sendMessage, "update", msg="-1") 
# end of class WatchdockFrame
    def onClose(self, event):
        self.Close()

    def OnExitApp(self, event):
        self.Destroy()


class CommitDialog(wx.Dialog):
    def __init__(self, cont_id, repo):
        self.cont_id=cont_id
        self.repo=repo
        # begin wxGlade: CommitDialog.__init__
        wx.Dialog.__init__(self, None, wx.ID_ANY,title="Save container change",style=wx.DEFAULT_DIALOG_STYLE,size=(470, 290))
        # self.txt_img_name_tag = wx.TextCtrl(self, wx.ID_ANY, "namespace/name:tag", style=wx.HSCROLL | wx.TE_DONTWRAP)
        self.txt_img_name_tag = wx.TextCtrl(self, wx.ID_ANY, repo)
        self.txt_your_name = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_commit_msg = wx.TextCtrl(self, wx.ID_ANY, "quick save", style=wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_WORDWRAP )
        self.btn_ok = wx.Button(self, wx.ID_ANY, "Commit")
        self.btn_cancel = wx.Button(self, wx.ID_ANY, "Cancel")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.OnTextedCommitMsg, self.txt_commit_msg)
        self.Bind(wx.EVT_BUTTON, self.OnClickedCommit, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.OnClickedCancel, self.btn_cancel)
        # end wxGlade
        pub.subscribe(self.OnMsgCommit, 'container.commit')


    def SetRepository(self, cont_id,repo):
        self.cont_id=cont_id
        self.repo=repo
        self.txt_img_name_tag.SetValue(repo)
        return 
    def GetTagValue(self):
        return self.txt_img_name_tag.GetValue()
    def GetNameValue(self):
        return self.txt_your_name.GetValue()
    def GetMsgValue(self):
        return self.txt_commit_msg.GetValue()
    def __set_properties(self):
        # begin wxGlade: CommitDialog.__set_properties
        self.is_virgin_commit_msg=True
        self.txt_img_name_tag.SetToolTipString("You can enter new string other than existed image name and tag")
        self.txt_commit_msg.SetMinSize((-1, 60))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CommitDialog.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.FlexGridSizer(1, 5, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(0, 4, 0, 0)
        sizer_10 = wx.FlexGridSizer(1, 3, 0, 0)
        sizer_3.Add((14, 6), 0, 0, 0)
        sizer_10.Add((14, 20), 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "\nSelected container '%s' will be commited to the image you designate.\nPlease enter repository name with a tag of the target image.\nCommit message and Your name are optional."%self.cont_id)
        sizer_10.Add(label_5, 1, wx.EXPAND, 0)
        sizer_10.Add((14, 20), 0, 0, 0)
        sizer_10.AddGrowableRow(0)
        sizer_10.AddGrowableCol(1)
        sizer_3.Add(sizer_10, 1, wx.EXPAND, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Repo name & tag")
        grid_sizer_1.Add(label_2, 0, 0, 0)
        grid_sizer_1.Add(self.txt_img_name_tag, 0, wx.EXPAND, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Your name")
        grid_sizer_1.Add(label_3, 0, 0, 0)
        grid_sizer_1.Add(self.txt_your_name, 0, wx.EXPAND, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Commit message")
        grid_sizer_1.Add(label_4, 0, 0, 0)
        grid_sizer_1.Add(self.txt_commit_msg, 0, wx.EXPAND, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableRow(2)
        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableCol(2)
        sizer_3.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_9.Add((0, 0), 0, 0, 0)
        sizer_9.Add((200, 40), 0, wx.EXPAND, 0)
        sizer_9.Add(self.btn_ok, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add(self.btn_cancel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add((20, 20), 0, wx.EXPAND, 0)
        sizer_9.AddGrowableCol(1)
        sizer_3.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_3.Add((20, 20), 0, 0, 0)
        self.SetSizer(sizer_3)
        self.Layout()
        # end wxGlade
        # label_5.Wrap()
    def OnTextedCommitMsg(self, event):  # wxGlade: CommitDialog.<event_handler>
        if self.is_virgin_commit_msg:
            self.txt_commit_msg.Clear()
            self.is_virgin_commit_msg=False

    def OnClickedCommit(self, event):  # wxGlade: CommitDialog.<event_handler>
        self.EndModal(wx.ID_OK)

        # self.onQuit(None)

    def OnClickedCancel(self, event):  # wxGlade: CommitDialog.<event_handler>
        self.EndModal(wx.ID_CANCEL)

    def OnMsgCommit(self,cmd):
        self.OnClickedCommit(None)
# end of class CommitDialog


class WatchdockApp(wx.App):

    def __init__(self, testing):
        super(WatchdockApp, self).__init__()
        self.testing=testing
        self.cov = None
        # self.cov = coverage.Coverage(omit="*/__init__.py",include="watchdock/*")
        # if self.testing:
        #     self.cov = coverage.Coverage(include="watchdock/*")
        #     self.cov.start()
        self.frame = WatchdockFrame(parent=None, testing=self.testing, id=wx.ID_ANY)
        # self.frame.set_test(testing) #must be called for initial refresh
        self.SetTopWindow(self.frame)
        # if not self.testing:
        self.frame.Show()


    def OnInit(self):
        return True

    def OnExitApp(self, event):
        self.Destroy()
    
    def Destroy(self):
        # if self.testing:
        #     self.cov.stop()
        #     self.cov.save()
        #     self.cov.report()
        #     self.cov.xml_report()
        #     self.cov.html_report()
        wx.PyApp.Destroy(self)
# end of class WatchdockApp

if __name__ == "__main__":
    app = WatchdockApp(testing=False)
    app.MainLoop()
    
