import unittest
import wx

import watchdock.run as run
import time
import coverage
# import testTopLevelWindow

class WatchdockTest(unittest.TestCase):

    def setUp(self):
        self.cov = coverage.Coverage( omit="*/__init__.py",include="watchdock/*")
        self.cov.start()
        app = wx.App()
        self.frame = run.WatchdockFrame(None, wx.ID_ANY, "")
        self.frame.set_test(True)

    def test_container_list(self):
        itemcnt = self.frame.lst_containers.GetCount()
        sout = self.frame.mockdata['docker container ls -a']
        assert itemcnt == len(sout.splitlines()[1:])

    def test_image_list(self):
        itemcnt = self.frame.lst_images.GetCount()
        sout = self.frame.mockdata['docker images']
        assert itemcnt == len(sout.splitlines()[1:])

    def test_container_selection(self):
        index=0
        self.frame.lst_containers.SetSelection(index)
        cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=self.frame.lst_containers.GetId())
        cmd.SetEventObject(self.frame.lst_containers)
        self.frame.ProcessEvent(cmd)
        # wx.PostEvent(self.frame, cmd)
        sout = self.frame.mockdata['docker container ls -a']
        # time.sleep(1)
        print("sout ==>",sout.splitlines()[index+1].decode('utf-8'))
        print("list ==>",self.frame.txt_details.GetLineText(0))
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

    def tearDown(self):
        self.cov.stop()
        self.cov.save()
        self.cov.report()
        self.cov.xml_report()

if __name__ == '__main__':

    unittest.main()
    