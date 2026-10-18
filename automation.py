"""Local auto-clicker with one configurable hotkey and no input recording."""
from contextlib import contextmanager
import ctypes as c
from ctypes import wintypes as w
import json
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

ULONG_PTR=w.WPARAM
class POINT(c.Structure): _fields_=[('x',w.LONG),('y',w.LONG)]
class MOUSE(c.Structure): _fields_=[('dx',w.LONG),('dy',w.LONG),('data',w.DWORD),('flags',w.DWORD),('time',w.DWORD),('extra',ULONG_PTR)]
class UNION(c.Union): _fields_=[('mouse',MOUSE)]
class INPUT(c.Structure): _fields_=[('type',w.DWORD),('u',UNION)]
user=c.WinDLL('user32',use_last_error=True)
kernel=c.WinDLL('kernel32',use_last_error=True)
user.SendInput.argtypes=[w.UINT,c.POINTER(INPUT),c.c_int];user.SendInput.restype=w.UINT
user.PostThreadMessageW.argtypes=[w.DWORD,w.UINT,w.WPARAM,w.LPARAM]

@contextmanager
def physical_pixels():
    previous=None
    try:
        user.SetThreadDpiAwarenessContext.argtypes=[c.c_void_p]
        user.SetThreadDpiAwarenessContext.restype=c.c_void_p
        previous=user.SetThreadDpiAwarenessContext(c.c_void_p(-4))
    except AttributeError:pass
    try:yield
    finally:
        if previous:user.SetThreadDpiAwarenessContext(previous)

BUTTONS={'left':(2,4),'right':(8,16),'middle':(32,64)}
KEYS={f'F{i}':111+i for i in range(1,13)}
DEFAULT={'interval_ms':100,'button':'left','double':False,'click_count':0,'fixed':False,'x':0,'y':0,'click_key':'F6'}

def config_valid(data):
    if not isinstance(data,dict):raise ValueError('Invalid configuration.')
    result={**DEFAULT,**{k:v for k,v in data.items() if k in DEFAULT}}
    for key,low,high in [('interval_ms',10,3600000),('click_count',0,10000000),('x',-100000,100000),('y',-100000,100000)]:
        value=result[key]
        if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:raise ValueError(f'Invalid {key}.')
    if result['button'] not in BUTTONS or any(type(result[k]) is not bool for k in ('double','fixed')):raise ValueError('Invalid click options.')
    if result['click_key'] not in KEYS:raise ValueError('Choose a function-key hotkey.')
    return result

class Native:
    def cursor(self):
        with physical_pixels():
            p=POINT();user.GetCursorPos(c.byref(p));return [p.x,p.y]
    def down(self,vk):return bool(user.GetAsyncKeyState(vk)&0x8000)
    def emit(self,kind,v):
        if kind=='move':
            # Virtual desktop mapping supports monitors with negative coordinates.
            with physical_pixels():x,y,width,height=[user.GetSystemMetrics(i) for i in (76,77,78,79)]
            dx=round((v[0]-x)*65535/max(1,width-1));dy=round((v[1]-y)*65535/max(1,height-1))
            item=INPUT(type=0,u=UNION(mouse=MOUSE(dx,dy,0,0xC001,0,0)))
        elif kind=='button':
            flags=BUTTONS[('left','right','middle')[v[0]]][0 if v[1] else 1]
            item=INPUT(type=0,u=UNION(mouse=MOUSE(0,0,0,flags,0,0)))
        else:raise ValueError('Unsupported click input.')
        if user.SendInput(1,c.byref(item),c.sizeof(INPUT))!=1:raise OSError('Windows blocked automated clicking. Use a target at the same permission level as PerfHub.')

class Engine:
    def __init__(self,native=None):
        self.native=native or Native();self.mode='idle';self.status='Ready';self.stop_event=threading.Event();self.thread=None
    def stop(self):self.stop_event.set()
    def start(self,mode,settings):
        if mode!='clicking':raise ValueError('Only auto clicking is supported.')
        if self.mode!='idle':raise ValueError('Stop the clicker first.')
        settings=config_valid(settings);self.mode='clicking';self.status='Clicking';self.stop_event=threading.Event()
        task_stop=self.stop_event
        self.thread=threading.Thread(target=self._run,args=(settings,task_stop),daemon=True);self.thread.start()
        def emergency():
            while self.stop_event is task_stop and self.mode!='idle' and not task_stop.wait(.02):
                if self.native.down(27):task_stop.set();return
        threading.Thread(target=emergency,daemon=True).start()
    def _run(self,settings,stop):
        held=None
        def emit(kind,values):
            nonlocal held
            self.native.emit(kind,values)
            if kind=='button':held=values[0] if values[1] else None
        try:
            count=0;which=('left','right','middle').index(settings['button'])
            while not stop.is_set():
                if settings['fixed']:emit('move',[settings['x'],settings['y']])
                for i in range(2 if settings['double'] else 1):
                    if stop.is_set():break
                    emit('button',[which,1]);emit('button',[which,0])
                    if settings['double'] and i==0 and stop.wait(.04):break
                count+=1;self.status=f'Clicking - {count} cycles'
                if settings['click_count'] and count>=settings['click_count']:break
                if stop.wait(settings['interval_ms']/1000):break
            self.status='Stopped' if stop.is_set() else 'Finished'
        except Exception as exc:self.status=str(exc)
        finally:
            if held is not None:
                try:self.native.emit('button',[held,0])
                except OSError:pass
            self.mode='idle'

class Hotkeys:
    """Dedicated Windows message loop; registered function keys are consumed by Windows."""
    def __init__(self,events):
        self.events=events;self.commands=queue.Queue();self.thread_id=0;self.closed=False
        self.thread=threading.Thread(target=self.run,daemon=True);self.thread.start()
    def update(self,settings):
        self.commands.put(dict(settings))
        if self.thread_id:user.PostThreadMessageW(self.thread_id,0x8001,0,0)
    def close(self):
        self.closed=True
        if self.thread_id:user.PostThreadMessageW(self.thread_id,0x12,0,0)
    def run(self):
        message=w.MSG();user.PeekMessageW(c.byref(message),None,0,0,0)
        self.thread_id=kernel.GetCurrentThreadId();active={}
        def unregister():
            user.UnregisterHotKey(None,1)
        def register(settings):
            if not user.RegisterHotKey(None,1,0x4000,KEYS[settings['click_key']]):return settings['click_key']
            return None
        try:
            while not self.closed:
                while not self.commands.empty():
                    requested=self.commands.get();unregister();failed=register(requested)
                    if failed:
                        unregister()
                        if active:register(active)
                        self.events.put(('hotkey_error',f'{failed} is already in use. Choose another key and apply hotkeys.'))
                    else:active=requested;self.events.put(('hotkeys',requested))
                if self.closed or user.GetMessageW(c.byref(message),None,0,0)<=0:break
                if message.message==0x312 and int(message.wParam)==1:self.events.put(('toggle','clicking'))
        finally:unregister();self.thread_id=0

class AutomationPage:
    def __init__(self,hub,tab,g,root_path):
        self.hub=hub;self.g=g;self.engine=Engine();self.pending=None;self.closed=False;self.root_path=root_path
        body=hub.page(tab,'Auto clicker','Set your click speed, button, position and repeat count. Your hotkey starts or stops clicking; Esc always stops.')
        self.vars={k:tk.BooleanVar(value=v) if type(v) is bool else tk.StringVar(value=str(v)) for k,v in DEFAULT.items()}
        self.status=hub.label(body,'Ready - F6: start / stop | Esc: stop',11)
        self.controls=hub.box(body,'Auto clicker','Choose an interval, button and repeat limit. Zero cycles means repeat until stopped.')
        for label,key in [('Interval (ms)','interval_ms'),('Click cycles (0 = unlimited)','click_count')]:self.field(self.controls,label,key)
        self.field(self.controls,'Mouse button','button',list(BUTTONS))
        self.check(self.controls,'Double click','double');self.check(self.controls,'Click at fixed coordinates','fixed')
        row=tk.Frame(self.controls,bg=g['PANEL']);row.pack(fill='x',padx=16,pady=4)
        self.field(row,'X','x');self.field(row,'Y','y')
        g['RButton'](self.controls,'Pick cursor position in 3 seconds',self.pick).pack(anchor='w',padx=16,pady=6)
        self.buttons(self.controls,[('Start / stop clicker',lambda:self.toggle('clicking')),('Stop clicking',self.stop)])
        settings=hub.box(body,'Hotkey & configuration','The start/stop hotkey works while PerfHub is open, including when another app has focus. Save and load your clicker settings.')
        self.field(settings,'Start / stop hotkey','click_key',list(KEYS))
        self.active_keys={'click_key':DEFAULT['click_key']}
        self.hotkey_events=queue.Queue();self.hotkeys=Hotkeys(self.hotkey_events);self.hotkeys.update(self.active_keys)
        self.buttons(settings,[('Apply hotkey',self.apply_keys),('Save configuration',self.save),('Load configuration',self.load)])
        hub.bind('<Destroy>',self.destroy,add='+');self.job=hub.after(25,self.poll)
    def field(self,parent,label,key,choices=None):
        row=tk.Frame(parent,bg=self.g['PANEL']);row.pack(fill='x',padx=16,pady=4)
        tk.Label(row,text=label,bg=self.g['PANEL'],fg=self.g['FG'],anchor='w',width=32).pack(side='left')
        if choices:
            entry=self.g['RSelect'](row,choices,width=220,command=self.vars[key].set)
            entry.set(self.vars[key].get())
            self.vars[key].trace_add('write',lambda *_,e=entry,k=key:e.set(self.vars[k].get()))
        else:entry=self.g['REntry'](row,self.vars[key],width_px=220)
        entry.pack(side='left')
    def check(self,parent,label,key):
        self.g['RCheck'](parent,label,self.vars[key]).pack(anchor='w',padx=16,pady=3)
    def buttons(self,parent,items):
        row=tk.Frame(parent,bg=self.g['PANEL']);row.pack(fill='x',padx=16,pady=8)
        for text,command in items:self.g['RButton'](row,text,command).pack(side='left',padx=(0,8))
    def settings(self):
        values={k:v.get() for k,v in self.vars.items()}
        for key in ('interval_ms','click_count','x','y'):values[key]=int(values[key])
        return config_valid(values)
    def apply_keys(self):
        if self.pending or self.engine.mode!='idle':
            messagebox.showinfo('Hotkeys','Stop clicking before changing the hotkey.',parent=self.hub);return
        try:
            config=self.settings();self.hotkeys.update({k:config[k] for k in self.active_keys});self.engine.status='Applying hotkey...'
        except ValueError as exc:messagebox.showerror('Hotkeys',str(exc),parent=self.hub)
    def stop(self):
        if self.pending:self.hub.after_cancel(self.pending);self.pending=None
        self.engine.stop();self.engine.status='Stopped'
    def toggle(self,mode='clicking'):
        if mode!='clicking':return
        if self.pending or self.engine.mode!='idle':self.stop();return
        try:
            settings=self.settings();settings.update(self.active_keys);self.engine.start('clicking',settings)
        except ValueError as exc:messagebox.showerror('Auto clicker',str(exc),parent=self.hub)
    def pick(self):
        if self.pending or self.engine.mode!='idle':return
        self.engine.status='Move the cursor to the target - capturing in 3 seconds'
        def capture():
            self.pending=None;x,y=self.engine.native.cursor();self.vars['x'].set(str(x));self.vars['y'].set(str(y));self.vars['fixed'].set(True);self.engine.status=f'Position selected: {x}, {y}'
        self.pending=self.hub.after(3000,capture)
    def save(self):
        if self.pending or self.engine.mode!='idle':messagebox.showinfo('Configuration','Stop clicking before saving.',parent=self.hub);return
        try:
            settings=self.settings();path=filedialog.asksaveasfilename(parent=self.hub,title='Save clicker configuration',defaultextension='.json',initialfile='PerfHub-clicker.json',filetypes=[('PerfHub configuration','*.json')])
            if path:
                from pathlib import Path
                Path(path).write_text(json.dumps({'version':2,'settings':settings},indent=2),encoding='utf-8');self.engine.status='Configuration saved'
        except (OSError,ValueError) as exc:messagebox.showerror('Save',str(exc),parent=self.hub)
    def load(self):
        if self.pending or self.engine.mode!='idle':messagebox.showinfo('Configuration','Stop clicking before loading.',parent=self.hub);return
        path=filedialog.askopenfilename(parent=self.hub,filetypes=[('PerfHub configuration','*.json')])
        if not path:return
        try:
            from pathlib import Path
            if Path(path).stat().st_size>20000000:raise ValueError('Configuration is too large.')
            data=json.loads(Path(path).read_text(encoding='utf-8'));settings=config_valid(data['settings'])
            if data.get('version') not in (1,2):raise ValueError('Unsupported configuration version.')
            for k,v in settings.items():self.vars[k].set(v)
            self.apply_keys();self.engine.status='Clicker settings loaded'
        except (OSError,ValueError,KeyError,TypeError) as exc:messagebox.showerror('Load',str(exc),parent=self.hub)
    def poll(self):
        if self.closed:return
        escape=self.engine.native.down(27)
        if escape:self.stop()
        while not self.hotkey_events.empty():
            kind,data=self.hotkey_events.get()
            if kind=='toggle' and not escape:self.toggle(data)
            elif kind=='hotkeys':self.active_keys=data;self.engine.status='Hotkey applied'
            else:self.engine.status=data
        self.status.config(text=f"{self.engine.status}\n{self.active_keys['click_key']}: start / stop | Esc: stop")
        self.job=self.hub.after(25,self.poll)
    def destroy(self,event):
        if event.widget is self.hub:
            self.closed=True;self.stop();self.hotkeys.close()
            if self.engine.thread:self.engine.thread.join(timeout=1)
            self.hotkeys.thread.join(timeout=1)
