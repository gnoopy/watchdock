
# from .context import watchdock
import pytest
import watchdock.run as run
import wx
import time
import coverage
from wx.lib.pubsub import pub

theapp=None

@pytest.fixture
def app():
    app = run.WatchdockApp(testing=True)
    return app
    # return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)


def test_container_list(app):
    itemcnt = app.frame.lst_containers.GetCount()
    sout = app.frame.mockdata["docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}'"]
    # print("itemcnt",itemcnt,"sout",sout)
    assert itemcnt == len(sout.splitlines()[1:])

def test_image_list(app):
    itemcnt = app.frame.lst_images.GetCount()
    sout = app.frame.mockdata['docker images']
    assert itemcnt == len(sout.splitlines()[1:])

def test_container_selection(app):
    index=1
    app.frame.lst_containers.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_containers.GetId())
    cmd.SetEventObject(app.frame.lst_containers)
    app.frame.ProcessEvent(cmd)
    sout = app.frame.mockdata["docker container ls -a --format 'table {{.ID}}  {{.Image}}\t{{.Names}}\t{{.Command}}\t{{.Status}}\t{{.Size}}'"]
    # time.sleep(1)
    # print("sout ==>",sout.splitlines()[index+1].decode('utf-8'))
    # print("list ==>",app.frame.txt_details.GetLineText(0))
    assert sout.splitlines()[index+1].decode('utf-8') == app.frame.txt_details.GetLineText(0)


def test_image_selection(app):
    index=0
    app.frame.lst_images.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_images.GetId())
    cmd.SetEventObject(app.frame.lst_images)
    # cmd.SetId(app.frame.lst_images.GetId())
    # cmd.SetInt(index)
    # cmd.SetString(app.frame.lst_images.GetString(index))
    app.frame.ProcessEvent(cmd)
    
    img_line = app.frame.lst_images.GetStringSelection()
    # img_id = img_line[46:58]
    img_id = app.frame.get_img_id(img_line)
    hst_cnt = app.frame.lst_images_hst.GetCount()
    sout=''
    if 'docker image history '+img_id in app.frame.mockdata.keys():
        sout = app.frame.mockdata['docker image history '+img_id]
    elif 'docker image history '+img_id+"\r" in app.frame.mockdata.keys():
        sout = app.frame.mockdata['docker image history '+img_id+"\r"]
    else:
        assert False
    # time.sleep(1)
    # print("sout cnt:",len(sout.splitlines()[1:]), " hst_cnt",hst_cnt)
    # print("sout ==>",sout.splitlines())
    # print("list ==>",app.frame.lst_images_hst)
    assert len(sout.splitlines()[1:]) - int(hst_cnt) == 0

def test_container_restart(app):
    index = 0
    app.frame.lst_containers.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_containers.GetId())
    cmd.SetEventObject(app.frame.lst_containers)
    app.frame.ProcessEvent(cmd)
    cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.btn_restart.GetId())
    cmd2.SetEventObject(app.frame.btn_restart)
    app.frame.btn_restart.ProcessEvent(cmd2)
    assert "docker container restart "+app.frame.cont_id == app.frame.last_cmd_out.strip() 

def test_container_start(app):
    index = 2
    app.frame.lst_containers.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_containers.GetId())
    cmd.SetEventObject(app.frame.lst_containers)
    app.frame.ProcessEvent(cmd)
    # cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.btn_start.GetId())
    # cmd2.SetEventObject(app.frame.btn_start)
    # app.frame.btn_start.ProcessEvent(cmd2)
    app.frame.OnClickedStart(None)
    assert "docker container start "+app.frame.cont_id == app.frame.last_cmd_out.strip() 

def test_container_stop(app):
    index = 0
    app.frame.lst_containers.SetSelection(index)
    cmd=wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_containers.GetId())
    cmd.SetEventObject(app.frame.lst_containers)
    app.frame.ProcessEvent(cmd)
    cmd2=wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.btn_stop.GetId())
    cmd2.SetEventObject(app.frame.btn_stop)
    app.frame.btn_stop.ProcessEvent(cmd2)
    assert "docker container stop "+app.frame.cont_id == app.frame.last_cmd_out.strip() 

def test_image_delete(app):
    index = 0
    app.frame.lst_images.SetSelection(index)
    cmd = wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_images.GetId())
    cmd.SetEventObject(app.frame.lst_images)
    app.frame.ProcessEvent(cmd)
    img_line = app.frame.lst_images.GetStringSelection()
    img_id = app.frame.get_img_id(img_line)

    cmd2 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.btn_del.GetId())
    cmd2.SetEventObject(app.frame.btn_del)
    app.frame.btn_del.ProcessEvent(cmd2)
    assert "docker image rm "+app.frame.img_id == app.frame.last_cmd_out.strip() 

def test_container_save(app):
    index = 0
    app.frame.lst_containers.SetSelection(index)
    cmd = wx.CommandEvent(commandEventType=wx.EVT_LISTBOX.evtType[0],id=app.frame.lst_containers.GetId())
    cmd.SetEventObject(app.frame.lst_containers)
    app.frame.ProcessEvent(cmd)
    
    name='My Test Name'
    msg='My Test Commit'
    # imgtag=app.frame.cmDlg.txt_img_name_tag.GetValue()
    app.frame.cmDlg.txt_your_name.SetValue(name)
    app.frame.cmDlg.OnTextedCommitMsg(None)
    app.frame.cmDlg.txt_commit_msg.SetValue(msg)
    theapp=app
    app.frame.cmDlg.Bind(wx.EVT_SHOW, OnShowCommitDlg, app.frame.cmDlg)

    cmd2 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.btn_save.GetId())
    cmd2.SetEventObject(app.frame.btn_save)
    app.frame.btn_save.ProcessEvent(cmd2)

    # cmd3 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=app.frame.cmDlg.btn_ok.GetId())
    # cmd3.SetEventObject(app.frame.cmDlg.btn_ok)
    # app.frame.cmDlg.btn_ok.ProcessEvent(cmd3)
    # time.sleep(1)
    imgtag=app.frame.cmDlg.repo
    expected = 'docker container commit -a "%s" -m "%s" %s %s'%(name, msg, app.frame.cmDlg.cont_id, imgtag)
    # print("expected:",expected)
    # print("result:", app.frame.last_cmd_out.strip())
    assert expected.replace('"','') == app.frame.last_cmd_out.strip().replace('"','')

def OnShowCommitDlg(event):
    print("OnShowCommitDlg called ##############################")
    cmDlg=event.GetEventObject()
    cmd3 = wx.CommandEvent(commandEventType=wx.EVT_BUTTON.evtType[0],id=cmDlg.btn_ok.GetId())
    cmd3.SetEventObject(cmDlg.btn_ok)
    cmDlg.btn_ok.ProcessEvent(cmd3)
    # pub.sendMessage('container.commit', cmd="")

