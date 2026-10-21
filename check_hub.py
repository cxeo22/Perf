"""Non-mutating checks. Never applies Windows tweaks."""
import perfhub as app
import hubplus
import automation
import time
from unittest.mock import Mock,patch
class TestHotkeys:
    def __init__(self,events):self.events=events;self.thread=Mock()
    def update(self,settings):self.events.put(('hotkeys',dict(settings)))
    def close(self):pass
automation.Hotkeys=TestHotkeys
def unexpected_dialog(title,message,**kwargs):raise AssertionError(f'{title}: {message}')
automation.messagebox.showerror=unexpected_dialog
app.Hub._load_info=lambda self:None
calls=[]
app.Hub.begin=lambda self,ids,mode,restore:calls.append((ids,mode))
hubplus.write_json=lambda *args:None
hubplus.install(vars(app))
hub=app.Hub(show_intro=False,enable_ai=False)
errors=[]
hub.report_callback_exception=lambda *args:errors.append(args)
hub.withdraw()
for i in range(len(hub.tabs)):
    hub.show_tab(i);hub.update()
hub._show_info({'cpu':'Test CPU','gpu':'Test GPU','ram':'16'},app.PRESET_ORDER[0],'Test recommendation',[])
hub.update()
assert len(hub.tabs)==28
assert len([n for n in hub.nav if n.winfo_manager()])==21
assert hub.nav[24].winfo_manager()=='pack'
assert hub.nav[25].winfo_manager()=='pack'
hub.nav[25].command()
assert hub.cur_tab==25
assert hub.builder_frame.winfo_manager()=='pack'
assert hub.nav[24].badge=='Beta'
hub.nav[24]._draw()
assert hub.nav[24].itemcget(hub.nav[24].find_withtag('nav-badge')[0],'text')=='Beta'
with patch.object(hub,'launch') as external:
    hub.nav[19].command()
    assert hub.cur_tab==19
    external.assert_not_called()
assert hub.nav[22].winfo_manager()=='pack'
assert hub.nav[23].winfo_manager()=='pack'
assert len(hub.app_starter.choices)==100
assert not hub.app_starter.runner.busy
hub.app_starter.mode._pick('Install apps')
assert hub.app_starter.start_button.label=='Install selected'
hub.app_starter.mode._pick('Download installers')
assert hub.app_starter.start_button.label=='Download selected'
with patch.object(hub.app_starter.runner,'start',return_value=False) as start:
    hub.app_starter.preset('Gaming')
    start.assert_not_called()
    assert hub.app_starter.visible==['chrome','epic','discord','steam','spotify','medal']
    hub.app_starter.choices['steam'].set(False)
    hub.app_starter.toggle_details('discord')
    assert 'Discord' in hub.app_starter.detail_text('discord')
    assert len(hub.app_starter.logos)==100
    hub.app_starter.start_selected()
    assert start.call_args.args[0]==['chrome','epic','discord','spotify','medal']
    assert start.call_args.args[1]=='download'
hub.app_starter.browse_all()
hub.app_starter.clear()
from drivers import components
driver_rows=components({'gpu':'NVIDIA GeForce RTX 4060'},[])
hub.drivers.event({'phase':'detected','rows':driver_rows,'status':'Test detected drivers'})
with patch('drivers.webbrowser.open') as open_browser:
    hub.drivers.open_link(driver_rows[0])
    assert open_browser.call_args.args[0]=='https://www.nvidia.com/en-us/drivers/'
    hub.drivers.open_link({**driver_rows[0],'url':'https://example.com/installer.exe'})
    assert open_browser.call_count==1
hub.drivers.event({'phase':'error','status':'Test offline fallback'})
assert hub.drivers.rows==driver_rows and not hub.drivers.busy
assert hub.nav[21].winfo_manager()=='pack'
assert hub.automation.engine.mode=='idle'
import tempfile,json
from pathlib import Path
from unittest.mock import patch
with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
    assert Path(directory).resolve().parent==Path(__file__).resolve().parent
    path=str(Path(directory)/'clicker.json')
    tool=hub.automation
    tool.vars['interval_ms'].set('250')
    tool.vars['click_key'].set('F9')
    with patch('automation.filedialog.asksaveasfilename',return_value=path):tool.save()
    assert json.loads(Path(path).read_text())['settings']['click_key']=='F9'
    tool.vars['interval_ms'].set('100')
    with patch('automation.filedialog.askopenfilename',return_value=path):tool.load()
    for _ in range(3):hub.update();time.sleep(.03)
    assert tool.vars['interval_ms'].get()=='250' and tool.active_keys['click_key']=='F9'
    saved_clicker=json.loads(Path(path).read_text())
    assert saved_clicker['version']==2 and 'events' not in saved_clicker
    assert set(tool.vars)==set(automation.DEFAULT) and not hasattr(tool.engine,'events')
    tool.pick()
    assert tool.pending and tool.engine.mode=='idle'
    tool.stop()
    assert tool.pending is None and tool.engine.mode=='idle'
assert hub.nav[20].winfo_manager()=='pack'
from unittest.mock import Mock,patch
assert not hasattr(hub,'open_ai')
bridge=Mock();bridge.process.poll.return_value=None;bridge.send.return_value=True
hub.ai_bridge=bridge;hub.ai_ready=True
hub.copy_ai_specs()
draft=bridge.send.call_args.args[0]
assert draft['op']=='insert' and 'CPU: Test CPU' in draft['text'] and 'GPU: Test GPU' in draft['text']
assert len(hub.help_ai_buttons)==len(app.HOW_STEPS)
for button,(title,body) in zip(hub.help_ai_buttons,app.HOW_STEPS):
    hub.show_tab(6)
    button.command()
    hub.update()
    guide_draft=bridge.send.call_args.args[0]
    assert guide_draft['op']=='insert' and title in guide_draft['text'] and body in guide_draft['text']
    assert 'troubleshoot this same method' in guide_draft['text']
    assert hub.tabs[20].winfo_manager()
    assert not hub.tabs[6].winfo_manager()
# Loading the assistant preserves guide context as a draft, without sending it.
hub.ai_ready=False
hub.help_ai_buttons[0].command()
assert app.HOW_STEPS[0][1] in hub.ai_pending[-1]
hub.ai_ready=True
hub.handle_ai_event({'type':'ready'})
assert not hub.ai_pending and bridge.send.call_args.args[0]['op']=='insert'
assert hub.nav[8].winfo_manager()=='pack'
assert hub.nav[19].winfo_manager()=='pack'
assert hub.nav[9].winfo_manager()=='pack'
assert hub.nav[17].winfo_manager()=='pack'
hub.preset_query.set('zzzz_no_preset_zzzz')
hub.update()
assert hub.preset_results==[]
hub.preset_query.set('')
hub.update()
assert len(hub.preset_results)==len(app.PRESET_ORDER)
hub.preset_browser();hub.update()
for child in hub.winfo_children():
    if isinstance(child,app.tk.Toplevel):child.destroy()
advanced=next(t['id'] for t in app.TWEAKS if t['risk']=='Advanced')
hub.begin([advanced],'apply',True)
assert calls==[([advanced],'apply')],calls
assert not hasattr(hub,'activate')
assert not hasattr(hub,'key_entry')
for name in ['Ember','Forest','Ember','Graphite','Midnight','Silver','Graphite']:
    hub.apply_theme(name)
    hub.update()
    assert hub.cget('bg')==hubplus.palette(name)['BG']
    assert bridge.update_theme.called
    def verify_roles(widget):
        for key,role in getattr(widget,'_theme_roles',{}).items():
            if role and key[0]=='option':
                assert widget.cget(key[1])==hubplus.palette(name)[role],(widget,key,name)
        for child in widget.winfo_children():verify_roles(child)
    verify_roles(hub)
    hub.open_preset(app.PRESET_ORDER[0]);hub.update()
    for child in hub.winfo_children():
        if isinstance(child,app.tk.Toplevel):child.destroy()
hub.apply_theme('Graphite')
from diagnostics import percentile
from renderbench import validate, TEST
assert percentile(250,[100,200,300,400])==50
assert percentile(200,[100,200,300])==50
assert percentile(50,[]) is None
hub.bench_history=[]
for fps in (10,20,30,25):
    result=validate({'test':TEST,'fps':fps,'low_fps':fps*.8,'duration':20,'frames':fps*20,'renderer':'Test GPU'})
    result.update(cpu='Test CPU',gpu='Test GPU',time='test')
    hub.show_benchmark(result)
assert 'Personal percentile: 67 / 100' in hub.bench_result.cget('text')
assert not hasattr(hub,'calculate_bottleneck')
assert not hasattr(hub,'cpu_benchmark')
for bad in (float('nan'),-1,0,float('inf')):
    try:validate({'test':TEST,'fps':bad,'low_fps':1,'duration':20,'frames':100})
    except ValueError:pass
    else:raise AssertionError('Invalid score accepted')
selected=next(iter(hub.customize_vars))
hub.customize_vars[selected].set(True)
hub.customize_search.set('zzzz_no_match')
hub.update()
hub.customize_search.set('')
hub.update()
assert hub.customize_vars[selected].get()
original_confirm=hubplus.messagebox.askyesno
hubplus.messagebox.askyesno=lambda *a,**k:True
hub.apply_customize('apply')
assert calls[-1]==([selected],'apply')
hubplus.messagebox.askyesno=original_confirm
hub.show_tab(18)
saved=[]
hubplus.write_json=lambda path,data:saved.append(data)
for style in hubplus.ANIMATIONS:
    hub.change_animation(style)
    for banner in hub.accents:
        if style=='Off':assert not banner.winfo_manager()
        original_viewable=banner.winfo_viewable
        banner.winfo_viewable=lambda:True
        banner.refresh()
        assert bool(banner.find_all())==(style!='Off')
        banner.winfo_viewable=original_viewable
    hub.update()
assert saved[-1]=={'theme':'Graphite','animation':'Grid'}
reveals=[]
original_reveal=hub.deiconify
hub.deiconify=lambda:reveals.append(True)
intro=hubplus.Intro(hub,{'BG':'#101214','ACC':'#69b4df'})
for _ in range(125):
    if intro.closed:break
    if intro.job:hub.after_cancel(intro.job);intro.job=None
    intro.tick()
assert intro.closed and len(reveals)==2
hub.deiconify=original_reveal
for metric in ('CPU','RAM','GPU'):
    hub.change_metric(metric);hub.update()
assert not errors,errors
hub.info={'cpu':'Test CPU','gpu':'Test GPU','ram':32,'raw':{'serial':'PRIVATE-SERIAL'},'username':'PRIVATE-USER'}
hub.ai_context_enabled.set(True)
context=hub.ai_context_message()
assert 'Test CPU' in context['snapshot'] and 'PRIVATE' not in context['snapshot']
hub.ai_context_enabled.set(False)
assert hub.ai_context_message()['snapshot']==''
hub.destroy()
print('PASS: 28 pages, idle automation, drivers page, AI draft/theme wiring (mocked), render validation, theme cycling, batch customization, animations and intro. No tuning applied.')
