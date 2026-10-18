"""Real startup mapping and focus checks. No network or tuning changes."""
import time
from unittest.mock import Mock
import perfhub as app
import hubplus
import automation

class Hotkeys:
    def __init__(self,*args):self.thread=Mock()
    def update(self,*args):pass
    def close(self):pass

automation.Hotkeys=Hotkeys
app.Hub._load_info=lambda self:None
hubplus.write_json=lambda *args:None
hubplus.install(vars(app))
hub=app.Hub(enable_ai=False)
errors=[]
hub.report_callback_exception=lambda *args:errors.append(args)
try:
    assert hub.show_intro and not hub.intro.closed
    hub.update()
    assert hub.state()=='withdrawn'
    assert hub.intro.window.winfo_ismapped()
    assert hub.focus_get() is hub.intro.window
    assert hub.intro.canvas.itemcget(hub.intro.word,'text')=='PerfHub'
    # Startup tab changes cannot steal focus from the visible opening screen.
    hub.show_tab(24);hub.update()
    assert hub.state()=='withdrawn' and hub.focus_get() is hub.intro.window
    intro=hub.intro
    while intro.frame<60:
        if intro.job:hub.after_cancel(intro.job);intro.job=None
        intro.tick()
    hub.update()
    assert intro.window.winfo_ismapped() and hub.state()=='withdrawn'
    assert intro.canvas.itemcget(intro.word,'fill')!='#101214'
    # Finish the unchanged fade/hold/dissolve, then return focus to the app.
    while not intro.closed:
        if intro.job:hub.after_cancel(intro.job);intro.job=None
        intro.tick()
    hub.update()
    assert hub.state()=='zoomed' and not intro.window.winfo_exists()
    hub.show_tab(24);hub.update()
    assert hub.focus_get() is hub
    assert not errors,errors
finally:
    hub.destroy()
print('PASS: opening screen visible and focused on startup, main app hidden until dissolve, original animation completes and normal tab focus resumes.')
