
# from .context import watchdock
import pytest
import watchdock.run as run
import wx
import time

@pytest.fixture
def frame():
    app = wx.PySimpleApp()
    frame = run.WatchdockFrame(None, wx.ID_ANY, "")
    frame.set_test(True)
    return frame
    # return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

def test_container_list(frame):
    itemcnt = frame.lst_containers.GetCount()
    sout = frame.mockdata['docker container ls -a']
    assert itemcnt == len(sout.splitlines()[1:])

def test_image_list(frame):
    itemcnt = frame.lst_images.GetCount()
    sout = frame.mockdata['docker images']
    assert itemcnt == len(sout.splitlines()[1:])

def test_container_selection(frame):
    index=2
    frame.lst_containers.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0])
    cmd.SetEventObject(frame.lst_containers)
    cmd.SetId(frame.lst_containers.GetId())
    cmd.SetInt(index)
    cmd.SetString(frame.lst_containers.GetString(index))
    frame.lst_containers.GetEventHandler().ProcessEvent(cmd)
    
    sout = frame.mockdata['docker container ls -a']
    # time.sleep(1)
    print("sout ==>",sout.splitlines()[index+1])
    print("list ==>",frame.txt_details.GetLineText(0))
    assert sout.splitlines()[index+1] == frame.txt_details.GetLineText(0)


def test_image_selection(frame):
    index=0
    frame.lst_images.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0])
    cmd.SetEventObject(frame.lst_images)
    cmd.SetId(frame.lst_images.GetId())
    cmd.SetInt(index)
    cmd.SetString(frame.lst_images.GetString(index))
    frame.lst_images.GetEventHandler().ProcessEvent(cmd)
    
    img_line = frame.lst_images.GetStringSelection()
    img_id = img_line[46:58]

    hst_cnt = frame.lst_images_hst.GetCount()
    sout = frame.mockdata['docker image history '+img_id]
    # time.sleep(1)
    # print("sout ==>",sout.splitlines())
    # print("list ==>",frame.lst_images_hst)
    assert len(sout.splitlines()[1:]) == hst_cnt
