"""Mixer UI checks with fake audio; never changes Windows audio settings."""
from unittest.mock import Mock
import tkinter as tk
import perfhub as app
import hubplus
import automation

class Hotkeys:
    def __init__(self,*args):self.thread=Mock()
    def update(self,*args):pass
    def close(self):pass

class FakeAudio:
    def __init__(self):self.writes=[]
    def snapshot(self):
        return dict(devices=[dict(key=('device',str(i)),id=str(i),flow=i%2,name='Test device '+str(i),level=40,mute=False,default=i<2,calls=i<2) for i in range(4)],
            sessions=[dict(key=('session','0','app'),name='Test app',device='Test output',level=65,mute=False)],errors=[])
    def set_level(self,key,value):self.writes.append(('level',key,float(value)))
    def set_mute(self,key,value):self.writes.append(('mute',key,value))
    def set_default(self,key,calls=False):self.writes.append(('default',key,calls))

automation.Hotkeys=Hotkeys
app.Hub._load_info=lambda self:None
hubplus.write_json=lambda *args:None
hubplus.install(vars(app))
hub=app.Hub(show_intro=False,enable_ai=False)
errors=[];hub.report_callback_exception=lambda *args:errors.append(args)
try:
    panel=hub.audio_panel;panel.backend=FakeAudio()
    hub.show_tab(27);panel.refresh();hub.update()
    assert len(hub.tabs)==28 and len(panel.views[0]['rows'])==3
    panel.refresh();hub.update();assert not panel.backend.writes
    panel.pop_out();hub.update();assert len(panel.views)==2
    panel.pop_out();assert len(panel.views)==2
    panel.refresh();hub.update();assert not panel.backend.writes
    panel.action_level(('session','0','app'),32,panel.views[0])
    assert panel.backend.writes[-1]==('level',('session','0','app'),32)
    panel.action(lambda:panel.backend.set_mute(('device','1'),True))
    assert panel.backend.writes[-1]==('mute',('device','1'),True)
    panel.action(lambda:panel.backend.set_default('2',True))
    assert panel.backend.writes[-1]==('default','2',True)
    panel.backend.snapshot=lambda:dict(devices=[],sessions=[],errors=[])
    panel.refresh();hub.update();assert not panel.views[0]['rows']
    for theme in ('Forest','Graphite'):hub.apply_theme(theme,save=False);hub.update()
    panel.window.event_generate('<<Unused>>')
    close=panel.window.protocol('WM_DELETE_WINDOW');panel.window.tk.call(close)
    hub.update();assert len(panel.views)==1 and panel.window is None
    assert not errors,errors
finally:hub.destroy()
assert panel.closed and panel.job is None
print('PASS: mixer tab, no refresh writes, synchronized pop-out, single window, volume/mute/default dispatch, unplugged devices, themes and cleanup.')
