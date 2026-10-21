from branding import feather
"""Local palettes and small canvas accents, without image or network dependencies."""
import math
import tkinter as tk

ANIMATIONS=('Off','Particles','Constellation','Fireflies','Double Helix','Orbit','Waves','Grid')

def blend(a,b,t):
    x=tuple(int(a[i:i+2],16) for i in (1,3,5));y=tuple(int(b[i:i+2],16) for i in (1,3,5))
    return '#%02x%02x%02x'%tuple(round(v+(z-v)*t) for v,z in zip(x,y))

THEMES={
    'Graphite':('#09090b','#101012','#151518','#222226','#303035','#eeeef0'),
    'Midnight':('#0c121b','#101925','#162130','#1e2e40','#2d435a','#71b7ed'),
    'Forest':('#101613','#151e19','#1b2720','#24352b','#344a3c','#7cc6a1'),
    'Ember':('#191310','#211a16','#2a211b','#372b23','#4d3c30','#e0aa72'),
    'Silver':('#1b1d20','#212428','#292d32','#343a40','#474f57','#c1cbd3'),
}

def palette(name):
    bg,side,panel,panel2,line,accent=THEMES.get(name,THEMES['Graphite'])
    return dict(BG=bg,SIDE=side,PANEL=panel,PANEL2=panel2,LINE=line,ACC=accent,
                HERO=panel2,HERO2=panel,HERO_EDGE=line,NAV_ACTIVE=panel2,
                NAV_HOVER=panel,EDGE_HOVER=accent,ACC2=accent)

def recolor(root,g,old,new):
    roles={old[k]:k for k in new if k in old}
    def resolve(value):return roles.get(value) if isinstance(value,str) else None
    # Preserve default widget colors when dialogs or new rows are created later.
    def defaults(fn):
        values=getattr(fn,'__defaults__',None)
        if values:
            bindings=getattr(fn,'_theme_defaults',None)
            if bindings is None:
                bindings=[resolve(v) for v in values];fn._theme_defaults=bindings
            fn.__defaults__=tuple(new[role] if role else v for role,v in zip(bindings,values))
    for obj in list(g.values()):
        if isinstance(obj,type) and obj.__module__==g['__name__']:
            for method in vars(obj).values():defaults(method)
        elif callable(obj):defaults(obj)
    style_roles=getattr(root,'_button_theme_roles',{})
    for kind,style in g['RButton'].KINDS.items():
        for key,value in style.items():
            role=style_roles.setdefault((kind,key),resolve(value))
            if role:style[key]=new[role]
    root._button_theme_roles=style_roles
    def visit(widget):
        bindings=getattr(widget,'_theme_roles',{})
        for option in ('bg','fg','insertbackground','selectbackground','highlightbackground'):
            try:
                value=widget.cget(option)
                role=bindings.setdefault(('option',option),resolve(value))
                if role:widget.configure(**{option:new[role]})
            except tk.TclError:pass
        for key,value in list(vars(widget).items()):
            role=bindings.setdefault(('attribute',key),resolve(value))
            if role:setattr(widget,key,new[role])
        if isinstance(widget,tk.Canvas):
            for item in widget.find_all():
                for option in ('fill','outline'):
                    try:
                        value=widget.itemcget(item,option)
                        role=bindings.setdefault(('item',item,option),resolve(value))
                        if role:widget.itemconfigure(item,**{option:new[role]})
                    except tk.TclError:pass
            live=set(widget.find_all())
            bindings={key:role for key,role in bindings.items() if key[0]!='item' or key[1] in live}
        widget._theme_roles=bindings
        for child in widget.winfo_children():visit(child)
    visit(root)
    g.update(new)
    # Repaint blended hover/active shades that are not exact palette colors.
    def repaint(widget):
        if isinstance(widget,g['Card']):
            if hasattr(widget,'_hov_base'):
                widget._hov_base=widget.edge
                widget._hov_color=g['mix'](new['LINE'],new['ACC'],0.55)
            from types import SimpleNamespace
            widget._on_size(SimpleNamespace(width=max(2,widget.winfo_width()),height=max(2,widget.winfo_height())))
        elif isinstance(widget,tuple(g[k] for k in ('RButton','NavItem','RCheck','RSelect','RScrollbar'))):
            widget._draw()
        elif isinstance(widget,g['Bar']):widget._draw(max(2,widget.winfo_width()))
        for child in widget.winfo_children():repaint(child)
    repaint(root)

class Accent(tk.Canvas):
    """Animation is limited to a short banner; hidden windows stop drawing."""
    def __init__(self,parent,colors,style):
        self.colors=colors;self.style=style;self.phase=0;self.job=None
        super().__init__(parent,height=64,bg=colors()['PANEL'],highlightthickness=0)
        self.bind('<Destroy>',self.dispose,add='+')
        self.tick()

    def dispose(self,event):
        if event.widget is self and self.job:
            self.after_cancel(self.job);self.job=None

    def tick(self):
        self.job=None
        mode=self.style()
        if self.winfo_viewable():
            self.delete('all')
            p=self.colors();self.configure(bg=p['PANEL'])
            w=max(200,self.winfo_width());t=self.phase
            if mode=='Waves':
                for row in range(3):
                    points=[]
                    for x in range(0,w+12,12):points.extend((x,31+row*9+math.sin(x/85+t+row)*10))
                    self.create_line(*points,fill=p['ACC'] if row==0 else p['LINE'],width=2,smooth=True)
            elif mode=='Particles':
                count=max(24,min(96,math.ceil(w/72)))
                for i in range(count):
                    x=((i+.5)*w/count+t*14)%w;y=12+(i*29)%42+math.sin(t+i)*5
                    self.create_oval(x,y,x+3,y+3,fill=p['ACC'] if i%4==0 else p['LINE'],outline='')
            elif mode=='Grid':
                for x in range(-64,w+64,32):
                    shift=(t*10)%32
                    self.create_line(x+shift,0,x+shift-40,64,fill=p['LINE'])
                self.create_line(0,46,w,46,fill=p['ACC'])
            elif mode=='Double Helix':
                strands=[[],[]]
                for x in range(8,w,8):
                    phase=x/44+t
                    ys=(32+19*math.sin(phase),32-19*math.sin(phase))
                    for i in (0,1):strands[i].extend((x,ys[i]))
                    if x%24==8:self.create_line(x,ys[0],x,ys[1],fill=p['LINE'])
                for i,points in enumerate(strands):
                    if len(points)>=4:self.create_line(*points,fill=p['ACC'] if i==0 else blend(p['PANEL'],p['ACC'],0.4),width=2,smooth=True)
            elif mode=='Constellation':
                count=max(18,min(64,math.ceil(w/85)))
                stars=[(((i+.5)*w/count+t*(3+i%3))%w,12+(i*19)%40+math.sin(t/2+i)*4) for i in range(count)]
                for i,(x,y) in enumerate(stars):
                    for xx,yy in stars[i+1:]:
                        if (x-xx)**2+(y-yy)**2<75**2:self.create_line(x,y,xx,yy,fill=p['LINE'])
                    self.create_oval(x-1,y-1,x+2,y+2,fill=blend(p['PANEL'],p['ACC'],0.65),outline='')
            elif mode=='Fireflies':
                count=max(18,min(96,math.ceil(w/83)))
                for i in range(count):
                    x=((i+.5)*w/count+t*7)%w;y=30+math.sin(t/2+i*2)*20
                    glow=0.2+0.55*(math.sin(t+i)+1)/2
                    self.create_oval(x-4,y-4,x+4,y+4,fill=blend(p['PANEL'],p['ACC'],glow*0.15),outline='')
                    self.create_oval(x-1,y-1,x+1,y+1,fill=blend(p['PANEL'],p['ACC'],glow),outline='')
            elif mode=='Orbit':
                for i in range(5):
                    cx=w*(i+0.5)/5
                    self.create_oval(cx-35,18,cx+35,46,outline=p['LINE'])
                    x=cx+35*math.cos(t+i);y=32+14*math.sin(t+i)
                    self.create_oval(x-2,y-2,x+2,y+2,fill=p['ACC'],outline='')
            self.phase+=0.05
        if mode!='Off':self.job=self.after(50,self.tick)

    def refresh(self):
        if self.job:self.after_cancel(self.job);self.job=None
        self.delete('all');self.tick()

class Intro:
    """Monochrome feather with orbiting lights, then reveal the ready app."""
    def __init__(self,root,colors):
        self.root=root;self.colors=colors;self.frame=0;self.job=None;self.closed=False
        self.window=tk.Toplevel(root)
        self.window.overrideredirect(True)
        width,height=1260,820
        width=min(width,root.winfo_screenwidth()-60);height=min(height,root.winfo_screenheight()-80)
        x=(root.winfo_screenwidth()-width)//2;y=(root.winfo_screenheight()-height)//2
        geometry=f'{width}x{height}+{x}+{y}'
        root.geometry(geometry);self.window.geometry(geometry)
        self.canvas=tk.Canvas(self.window,bg=colors['BG'],highlightthickness=0)
        self.canvas.pack(fill='both',expand=True)
        import tkinter.font as tkfont
        families=set(tkfont.families(root))
        face=next((f for f in ('Segoe UI Variable Display','Bahnschrift','Segoe UI') if f in families),'Segoe UI')
        self.feather_frames=[feather(self.window,96,i) for i in range(21)]
        self.center=(width/2,height/2-98)
        cx,cy=self.center
        self.rings=[]
        for rx,ry in ((78,46),(64,76)):
            self.rings.append(self.canvas.create_oval(cx-rx,cy-ry,cx+rx,cy+ry,outline=colors['BG']))
        self.sparks=[self.canvas.create_oval(0,0,0,0,fill=colors['BG'],outline='') for _ in range(6)]
        self.feather=self.canvas.create_image(width/2,height/2-98,image=self.feather_frames[0])
        self.word=self.canvas.create_text(width/2,height/2-5,text='PerfHub',font=(face,46,'bold'),fill=colors['BG'])
        self.subtitle=self.canvas.create_text(width/2,height/2+52,text='YOUR PERFORMANCE WORKSPACE',font=('Segoe UI',10),fill=colors['BG'])
        self.track=self.canvas.create_line(cx-40,height/2+90,cx+40,height/2+90,fill=colors['BG'],width=2)
        self.progress=self.canvas.create_line(cx-40,height/2+90,cx-40,height/2+90,fill=colors['BG'],width=2)
        self.window.bind('<Escape>',lambda e:self.finish())
        self.window.bind('<Button-1>',lambda e:self.finish())
        self.window.bind('<Destroy>',self.destroyed,add='+')
        self.present_job=self.root.after_idle(self.present)
        self.tick()

    def present(self):
        self.present_job=None
        if self.closed:return
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def destroyed(self,event):
        if event.widget is self.window and self.present_job:
            self.root.after_cancel(self.present_job);self.present_job=None
        if event.widget is self.window and self.job:
            self.root.after_cancel(self.job);self.job=None

    def tick(self):
        if self.closed:return
        self.job=None;self.frame+=1
        # About 3.6 seconds: soft reveal, readable hold, then a slow dissolve.
        fade=max(0,min(1,(self.frame-8)/35))
        fade=fade*fade*(3-2*fade)
        self.canvas.itemconfigure(self.feather,image=self.feather_frames[round(fade*20)])
        self.canvas.itemconfigure(self.word,fill=blend(self.colors['BG'],'#edf1f4',fade))
        self.canvas.itemconfigure(self.subtitle,fill=blend(self.colors['BG'],self.colors['ACC'],fade*0.8))
        cx,cy=self.center
        self.canvas.coords(self.feather,cx,cy-4*math.sin(self.frame/12))
        for ring in self.rings:self.canvas.itemconfigure(ring,outline=blend(self.colors['BG'],'#ffffff',fade*.10))
        # Two lights follow offset elliptical paths, each with a short fading trail.
        for i,item in enumerate(self.sparks):
            orbit,trail=divmod(i,3)
            angle=self.frame*.065+orbit*math.pi-trail*.12
            rx,ry=((78,46),(64,76))[orbit]
            x,y=cx+rx*math.cos(angle),cy+ry*math.sin(angle)
            radius=2.3 if trail==0 else 1.4
            self.canvas.coords(item,x-radius,y-radius,x+radius,y+radius)
            self.canvas.itemconfigure(item,fill=blend(self.colors['BG'],'#f5f5f6',fade*(.9 if trail==0 else .28/trail)))
        self.canvas.itemconfigure(self.track,fill=blend(self.colors['BG'],'#333338',fade))
        self.canvas.itemconfigure(self.progress,fill=blend(self.colors['BG'],'#eeeef0',fade))
        self.canvas.coords(self.progress,cx-40,cy+188,cx-40+80*min(1,self.frame/85),cy+188)
        if self.frame==85:
            self.root.deiconify();self.window.lift()
        if self.frame>=85:
            try:self.window.attributes('-alpha',max(0,1-(self.frame-85)/35))
            except tk.TclError:
                self.finish();return
        if self.frame>=120:self.finish();return
        self.job=self.root.after(30,self.tick)

    def finish(self):
        if self.closed:return
        self.closed=True
        if self.job:self.root.after_cancel(self.job);self.job=None
        self.window.destroy();self.root.deiconify()
