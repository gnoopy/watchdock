import unittest
import wx

import watchdock.run as run
import time
import coverage
from wx.lib.pubsub import pub
# import testTopLevelWindow

class WatchdockTest(unittest.TestCase):

    def setUp(self):
        # self.cov = coverage.Coverage(omit="*/__init__.py",include="watchdock/*")
        # self.cov.start()
        self.app = run.WatchdockApp(testing=True)
        self.frame = self.app.frame #run.WatchdockFrame(None, wx.ID_ANY, "")

        # self.app.MainLoop()
        # self.frame.set_test(True)

    def test_container_list(self):
        itemcnt = self.frame.lst_containers.GetCount()
        sout = self.frame.mockdata["docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}'"]
        # print("itemcnt",itemcnt,"sout",sout)
        assert itemcnt == len(sout.splitlines()[1:])

    def test_image_list(self):
        itemcnt = self.frame.lst_images.GetCount()
        sout = self.frame.mockdata['docker images']
        assert itemcnt == len(sout.splitlines()[1:])

    def test_container_selection(self):
        index=1
        self.frame.lst_containers.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        sout = self.frame.mockdata["docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}'"]
        # time.sleep(1)
        # print("sout ==>",sout.splitlines()[index+1].decode('utf-8'))
        # print("list ==>",self.frame.txt_details.GetLineText(0))
        assert sout.splitlines()[index+1].decode('utf-8') == self.frame.txt_details.GetLineText(0)


    def test_image_selection(self):
        index=0
        self.frame.lst_images.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_images.GetId())
        cmd.SetEventObject(self.frame.lst_images)
        # cmd.SetId(self.frame.lst_images.GetId())
        # cmd.SetInt(index)
        # cmd.SetString(self.frame.lst_images.GetString(index))
        self.frame.ProcessEvent(cmd)
        
        img_line = self.frame.lst_images.GetStringSelection()
        # img_id = img_line[46:58]
        img_id = self.frame.get_img_id(img_line)
        hst_cnt = self.frame.lst_images_hst.GetCount()
        sout = self.frame.mockdata['docker image history '+img_id]
        # time.sleep(1)
        # print("sout cnt:",len(sout.splitlines()[1:]), " hst_cnt",hst_cnt)
        # print("sout ==>",sout.splitlines())
        # print("list ==>",self.frame.lst_images_hst)
        assert len(sout.splitlines()[1:]) - int(hst_cnt) == 0

    def test_container_restart(self):
        index = 0
        self.frame.lst_containers.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.btn_restart.GetId())
        cmd2.SetEventObject(self.frame.btn_restart)
        self.frame.btn_restart.ProcessEvent(cmd2)
        assert "docker container restart "+self.frame.cont_id == self.frame.last_cmd_out.strip() 

    def test_container_start(self):
        index = 2
        self.frame.lst_containers.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        # cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.btn_start.GetId())
        # cmd2.SetEventObject(self.frame.btn_start)
        # self.frame.btn_start.ProcessEvent(cmd2)
        self.frame.OnClickedStart(None)
        assert "docker container start "+self.frame.cont_id == self.frame.last_cmd_out.strip() 

    def test_container_stop(self):
        index = 0
        self.frame.lst_containers.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.btn_stop.GetId())
        cmd2.SetEventObject(self.frame.btn_stop)
        self.frame.btn_stop.ProcessEvent(cmd2)
        assert "docker container stop "+self.frame.cont_id == self.frame.last_cmd_out.strip() 

    def test_image_delete(self):
        index = 0
        self.frame.lst_images.SetSelection(index)
        cmd = wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_images.GetId())
        cmd.SetEventObject(self.frame.lst_images)
        self.frame.ProcessEvent(cmd)
        img_line = self.frame.lst_images.GetStringSelection()
        img_id = self.frame.get_img_id(img_line)

        cmd2 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.btn_del.GetId())
        cmd2.SetEventObject(self.frame.btn_del)
        self.frame.btn_del.ProcessEvent(cmd2)
        assert "docker image rm "+self.frame.img_id == self.frame.last_cmd_out.strip() 

    def test_container_save(self):
        index = 0
        self.frame.lst_containers.SetSelection(index)
        cmd = wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        
        name='My Test Name'
        msg='My Test Commit'
        # imgtag=self.frame.cmDlg.txt_img_name_tag.GetValue()
        self.frame.cmDlg.txt_your_name.SetValue(name)
        self.frame.cmDlg.OnTextedCommitMsg(None)
        self.frame.cmDlg.txt_commit_msg.SetValue(msg)

        self.frame.cmDlg.Bind(wx.EVT_SHOW, self.OnShowCommitDlg, self.frame.cmDlg)

        cmd2 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.btn_save.GetId())
        cmd2.SetEventObject(self.frame.btn_save)
        self.frame.btn_save.ProcessEvent(cmd2)

        # cmd3 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=self.frame.cmDlg.btn_ok.GetId())
        # cmd3.SetEventObject(self.frame.cmDlg.btn_ok)
        # self.frame.cmDlg.btn_ok.ProcessEvent(cmd3)
        # time.sleep(1)
        imgtag=self.frame.cmDlg.repo
        expected = 'docker container commit -a "%s" -m "%s" %s %s'%(name, msg, self.frame.cmDlg.cont_id, imgtag)
        # print("expected:",expected)
        # print("result:", self.frame.last_cmd_out.strip())
        assert expected.replace('"','') == self.frame.last_cmd_out.strip() 

    def OnShowCommitDlg(self, event):
        pub.sendMessage('container.commit', cmd="")

    def tearDown(self):
        self.frame.Close()
        # self.app.Close()
        self.app.Destroy()
        # self.cov.stop()
        # self.cov.save()
        # self.cov.report()
        # self.cov.xml_report()
        # self.cov.html_report()

#/cc-test-reporter after-build --exit-code 0 -t coverage.py -r $CC_TEST_REPORTER_ID
if __name__ == '__main__':
    unittest.main()
    