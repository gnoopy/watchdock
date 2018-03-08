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
		self.start()  # start the thread


	def run(self):
		"""Run Worker Thread."""
		wx.MilliSleep(100)
		pub.sendMessage("update", msg="")

class MyProgressDialog(wx.lib.agw.pyprogress.PyProgress):
	""""""
	
	def __init__(self, act_msg):
		"""Constructor"""
		wx.lib.agw.pyprogress.PyProgress.__init__(self, None, -1, "Command Execution",
		act_msg,
		agwStyle=wx.PD_APP_MODAL)
		self.SetGaugeSteps(50)
		self.SetGaugeBackground(wx.WHITE)
		self.SetGaugeProportion(0.2)
		self.SetFirstGradientColour(wx.WHITE)
		self.SetSecondGradientColour(wx.GREY)
		self.SetSize(300, self.GetSize()[1])
		self.stopNow = False
		# create a pubsub listener
		pub.subscribe(self.updateProgress, "update")
	
	def updateProgress(self, msg):
		"""
		Update the progress bar
		"""
		if msg == "-1":
			self.stopNow = True
			wx.MilliSleep(50)
			self.Hide()
			self.Destroy()
			wx.SafeYield()
			wx.GetApp().GetTopWindow().Raise()
		else:
			keepGoing = True
			while keepGoing:
				wx.MilliSleep(30)
				if self.stopNow:
					break
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
		font1 = wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
										wx.FONTWEIGHT_NORMAL, False, u'Monaco')
		font_header = wx.Font(
				9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, u'Monaco')

		pnl_root = wx.Panel(self)

		lbl_stats = wx.StaticText(pnl_root, label="Commands")
		lbl_containers = wx.StaticText(pnl_root, label="Containers")
		lbl_images = wx.StaticText(pnl_root, label="Images")
		lbl_dockersys = wx.StaticText(pnl_root, label="System")

		pnl_container = wx.Panel(pnl_root)
		vbox_container = wx.BoxSizer(wx.VERTICAL)
		self.txt_details = wx.TextCtrl(pnl_container, style=wx.TE_MULTILINE)
		self.cmd_cont_info = self.run_cmd_sync('docker container ls -a')
		if "Cannot connect to the Docker daemon" in self.cmd_cont_info or " the docker daemon is not running"  in self.cmd_cont_info:
			dlg = wx.MessageDialog(parent=None, message="Please run the docker service before run Simple Docker Dashboard"
				, caption="Error", style=wx.OK|wx.ICON_EXCLAMATION)
			dlg.ShowModal()
			dlg.Destroy()
			exit()
		lines = self.cmd_cont_info.splitlines()
		self.lst_containers = wx.ListBox(pnl_container, size=(100, -1),
																		choices=lines[1:], style=wx.LB_SINGLE)
		# lst = wx.ListBox(pnl_container, size = (100,-1), choices = [], style = wx.LB_SINGLE)

		lbl_cont_header = wx.StaticText(
				pnl_container, size=(100, -1), label=lines[0])
		self.txt_details.SetFont(font1)
		self.lst_containers.SetFont(font1)
		lbl_cont_header.SetFont(font1)
		vbox_container.Add(lbl_cont_header, 0, wx.EXPAND)
		vbox_container.Add(self.lst_containers, 1, wx.EXPAND)
		vbox_container.Add(self.txt_details, 2, wx.EXPAND)
		pnl_container.SetSizer(vbox_container)
		pnl_container.Fit()
		pnl_root.Bind(wx.EVT_LISTBOX, self.onListBox, self.lst_containers)

		self.tc3 = wx.TextCtrl(
				pnl_root, style=wx.TE_MULTILINE | wx.TE_READONLY)

		self.img_id=None
		pnl_images = wx.Panel(pnl_root)
		# self.txt_images = wx.TextCtrl(pnl_images, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.cmd_imgs_info = self.run_cmd_sync('docker images')
		# print(self.cmd_imgs_info)
		# print("-----------------------------------")
		(pnl_lst_images,self.lst_images)=self.simple_list(font_header,font1, self.cmd_imgs_info, pnl_images, self.onImgListBox)
		cmd_img_history=None
		if len(self.lst_images.GetItems()) != 0:
			self.lst_images.SetSelection(0)
			id=self.get_img_id(self.lst_images.GetStringSelection())
			cmd_img_history=self.get_img_history_str(id)
		(pnl_lst_image_history,self.lst_images_hst)=self.simple_list(font_header,font1, cmd_img_history, pnl_images, self.onImgHistBox)
		# pnl_lst_images.SetBackgroundColour(wx.GREEN)
		hbox_images = wx.BoxSizer(wx.HORIZONTAL)
		hbox_images.Add(pnl_lst_images,0, flag=wx.EXPAND)
		hbox_images.Add(pnl_lst_image_history,1, flag=wx.EXPAND)
		# pnl_lst_image_history.SetBackgroundColour(wx.RED)
		# self.lst_images_hst.SetBackgroundColour(wx.YELLOW)
		pnl_images.SetSizer(hbox_images)
		pnl_images.Fit()
		# self.lst_images.SetSelection(0)
		# self.lst_images.Select(0)
		# self.lst_images.Select(1)


		pnl_buttons = wx.Panel(pnl_root)
		self.btn_refresh = wx.Button(pnl_buttons, -1, "refresh")
		self.btn_stop = wx.Button(pnl_buttons, -1, "stop")
		self.btn_restart = wx.Button(pnl_buttons, -1, "restart")
		self.btn_start = wx.Button(pnl_buttons, -1, "start")
		self.btn_del = wx.Button(pnl_buttons, -1, "delete")
		self.btn_stop.Disable()
		self.btn_restart.Disable()
		self.btn_start.Disable()
		self.btn_del.Disable()

		hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
		pnl_buttons.SetSizer(hbox_buttons)
		hbox_buttons.AddSpacer(10)
		hbox_buttons.Add(self.btn_refresh, 0, wx.ALIGN_CENTER)
		hbox_buttons.AddSpacer(10)
		hbox_buttons.Add(self.btn_stop, 0, wx.ALIGN_CENTER)
		hbox_buttons.Add(self.btn_restart, 0, wx.ALIGN_CENTER)
		hbox_buttons.Add(self.btn_start, 0, wx.ALIGN_CENTER)
		hbox_buttons.AddSpacer(10)
		hbox_buttons.Add(self.btn_del, 0, wx.ALIGN_CENTER)

		self.btn_refresh.Bind(wx.EVT_BUTTON, self.OnClickedRefresh)
		self.btn_stop.Bind(wx.EVT_BUTTON, self.OnClickedStop)
		self.btn_restart.Bind(wx.EVT_BUTTON, self.OnClickedRestart)
		self.btn_start.Bind(wx.EVT_BUTTON, self.OnClickedStart)
		# self.btn_del.Bind(wx.EVT_BUTTON,self.OnclickedSave)
		self.btn_del.Bind(wx.EVT_BUTTON,self.OnclickedDelete)

		# self.txt_images.SetFont(font1)
		self.tc3.SetFont(font1)
		pnl_buttons.SetFont(font1)

		self.cmd_df_info = self.run_cmd_sync('docker system df')
		# self.txt_images.SetValue(self.cmd_imgs_info)
		self.tc3.SetValue(self.cmd_df_info)
		# self.run_command('docker lbl_stats',tc4)

		hbox_root = wx.BoxSizer(wx.HORIZONTAL)
		fgs = wx.FlexGridSizer(4, 2, 0, 0)
		fgs.AddMany([(lbl_stats), (pnl_buttons, 1, wx.EXPAND),
								(lbl_containers), (pnl_container, 1, wx.EXPAND),
								(lbl_images), (pnl_images, 1, wx.EXPAND),
								(lbl_dockersys), (self.tc3, 1, wx.EXPAND)])
		fgs.AddGrowableRow(0, 1)
		fgs.AddGrowableRow(1, 1)
		fgs.AddGrowableRow(2, 1)
		fgs.AddGrowableRow(3, 1)
		fgs.AddGrowableCol(1, 1)

		hbox_root.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
		pnl_root.SetSizer(hbox_root)

	def get_img_id(self, img_line):
		self.img_id = img_line[46:58]
		return self.img_id
	
	def get_img_history_str(self, id):
		str_history = self.run_cmd_sync('docker image history '+id+'')
		# lines = str_history.splitlines()
		return str_history

	def simple_list(self, h_font,l_font, str_items, pnl_parent, evt_handler):
		pnl_simplist = wx.Panel(pnl_parent)
		vbox_simplist = wx.BoxSizer(wx.VERTICAL)
		str_header=" "
		lines=[]
		if str_items is not None:
			lines = str_items.splitlines()
			str_header= lines[0]
		lst_simplist = wx.ListBox(pnl_simplist, choices=lines[1:], style=wx.LB_SINGLE)
		#  if str_items is None or len(str_items.strip()) == 0 else lines[0]
		# print("header :"+lines[0])
		lbl_header = wx.StaticText(pnl_simplist, label=str_header)

		lst_simplist.SetFont(l_font)
		lbl_header.SetFont(h_font)
		vbox_simplist.Add(lbl_header, 0, wx.EXPAND)
		vbox_simplist.Add(lst_simplist, 1, wx.EXPAND)
		pnl_simplist.SetSizer(vbox_simplist)
		pnl_simplist.Fit()
		pnl_simplist.Bind(wx.EVT_LISTBOX, evt_handler, lst_simplist)
		return pnl_simplist,lst_simplist

	def OnClickedStop(self, event):
		ProgressThread()
		dlg = MyProgressDialog("Stopping container... ")
		threading.Thread(target=self.stop, args=[self.cont_id]).start()


	def OnClickedRestart(self, event):
		ProgressThread()
		dlg = MyProgressDialog("ReStarting container... ")
		threading.Thread(target=self.restart, args=[self.cont_id]).start()
		# self.restart(self.cont_id)


	def OnClickedStart(self, event):
		ProgressThread()
		dlg = MyProgressDialog("Starting container... ")
		threading.Thread(target=self.start, args=[self.cont_id]).start()
		# self.start(self.cont_id)

	def OnClickedRefresh(self, event):
		self.refresh()
		# btn = event.GetEventObject().GetLabel()
		# print "Label of pressed button = ", btn

	def OnclickedDelete(self, event):
		self.run_cmd_sync('docker image rm '+self.img_id)
		self.refresh()
		self.btn_del.Disable()
		

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
		self.lst_images.IsSelected=False
		self.cont_id = None
		sout = self.run_cmd_sync('docker container ls -a')
		if self.cmd_cont_info != sout:
			lines = sout.splitlines()
			self.lst_containers.SetItems(lines[1:])
			self.btn_start.Disable()
			self.btn_restart.Disable()
			self.btn_stop.Disable()

		sout = self.run_cmd_sync('docker images')
		if self.cmd_imgs_info != sout:
			lines = sout.splitlines()
			self.lst_images.SetItems(lines[1:])
			# self.lst_images.SetSelection(0)
			if self.lst_images.IsSelected:
				id=self.get_img_id(self.lst_images.GetStringSelection())
				sout=self.get_img_history_str(id)
				lines = sout.splitlines()
				self.lst_images_hst.SetItems(lines[1:])
			else:
				self.lst_images_hst.SetItems([])
			self.btn_del.Disable()

		sout = self.run_cmd_sync('docker system df')
		if self.cmd_df_info != sout:
			self.tc3.SetValue(sout)

		pub.sendMessage("update", msg="-1")
		# wx.CallAfter(pub.sendMessage, "update", msg="-1")

	def onImgListBox(self, event):
		img_line = event.GetEventObject().GetStringSelection()
		self.img_id = img_line[46:58]
		print("img id :"+str(self.img_id)+"-----------------")
		str_history = self.run_cmd_sync('docker image history '+self.img_id+'')
		lines = str_history.splitlines()
		self.lst_images_hst.SetItems(lines[1:])
		self.btn_del.Enable()

	def onImgHistBox(self, event):
		pass

	def onListBox(self, event):
		self.container_line = event.GetEventObject().GetStringSelection()
		self.cont_id = self.container_line[0:12]
		top = self.run_cmd_sync('docker container top '+self.cont_id)+"----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
		logs = self.run_cmd_sync('docker container logs '+self.cont_id+'')
		self.txt_details.SetValue(self.container_line+"\n"+top+logs)
		if "Up" in self.container_line and "Exited (" not in self.container_line:
			self.btn_stop.Enable()
			self.btn_restart.Enable()
		else:
			self.btn_stop.Disable()
			self.btn_restart.Disable()
			self.btn_start.Enable()

	def run_cmd_sync(self, command):
		process = subprocess.Popen(shlex.split(
				command.encode('ascii','ignore')), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		tup = process.communicate()
		stdout = tup[0]+tup[1]
		# print("tup--> "+str(tup))
		return stdout

if __name__ == '__main__':
	app = wx.App()
	frame = DockerDashBoard(None, title='Simple Docker Dashboard')
	app.MainLoop()
