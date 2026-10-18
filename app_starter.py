"""App Starter: deliberate batch downloads/installs through Windows Package Manager."""
import html
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import threading
import time
import tkinter as tk
from urllib.parse import urlsplit
from urllib.request import Request,build_opener,HTTPRedirectHandler

# Exact identifiers verified against microsoft/winget-pkgs; never fuzzy-match apps.
CATALOG=[
 ('chrome','Google Chrome','Browser','Google.Chrome','https://www.google.com/chrome/'),
 ('epic','Epic Games Launcher','Games','EpicGames.EpicGamesLauncher','https://store.epicgames.com/download'),
 ('discord','Discord','Chat','Discord.Discord','https://discord.com/download'),
 ('steam','Steam','Games','Valve.Steam','https://store.steampowered.com/about/'),
 ('spotify','Spotify','Music','Spotify.Spotify','https://www.spotify.com/download/windows/'),
 ('drive','Google Drive','File sync','Google.GoogleDrive','https://www.google.com/drive/download/'),
 ('nvidia','NVIDIA App','For NVIDIA graphics cards',None,'https://www.nvidia.com/en-us/software/nvidia-app/'),
 ('afterburner','MSI Afterburner','GPU monitoring','Guru3D.Afterburner','https://www.msi.com/Landing/afterburner/graphics-cards'),
 ('logitech','Logitech G HUB','Logitech devices','Logitech.GHUB','https://www.logitechg.com/ghub'),
 ('rgb','SignalRGB','RGB lighting','WhirlwindFX.SignalRgb','https://signalrgb.com/'),
 ('capcut','CapCut','Video editing','ByteDance.CapCut','https://www.capcut.com/'),
 ('obs','OBS Studio','Recording and streaming','OBSProject.OBSStudio','https://obsproject.com/download'),
 ('medal','Medal','Game clips','MedalB.V.Medal','https://medal.tv/download')]
APPS={r[0]:r for r in CATALOG}
PRESETS={
 'Everyday':('chrome','discord','spotify','drive'),
 'Gaming':('chrome','epic','discord','steam','spotify','medal'),
 'Creator':('chrome','drive','capcut','obs','medal'),
 'Full setup':tuple(APPS)}


def winget_path():
    found=shutil.which('winget.exe')
    if found:return found
    candidate=Path(os.environ.get('LOCALAPPDATA',''))/'Microsoft/WindowsApps/winget.exe'
    return str(candidate) if candidate.is_file() else None


def command(executable,key,mode,destination):
    if key not in APPS or not APPS[key][3]:raise ValueError('Unknown package')
    if mode not in ('download','install'):raise ValueError('Unknown action')
    args=[executable,mode,'--id',APPS[key][3],'--exact','--source','winget','--accept-source-agreements','--accept-package-agreements','--disable-interactivity']
    if mode=='download':args+=['--download-directory',str(Path(destination)/key)]
    else:args+=['--silent']
    return args


def nvidia_url(url):
    try:
        p=urlsplit(url);host=(p.hostname or '').lower()
        return p.scheme=='https' and not p.username and not p.password and p.port in (None,443) and (host=='nvidia.com' or host.endswith('.nvidia.com'))
    except ValueError:return False


class NvidiaRedirect(HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,msg,headers,newurl):
        if not nvidia_url(newurl):raise ValueError('Download left NVIDIA’s official site')
        return super().redirect_request(request,fp,code,msg,headers,newurl)


def nvidia_link():
    opener=build_opener(NvidiaRedirect())
    req=Request(APPS['nvidia'][4],headers={'User-Agent':'PerfHub App Starter/1.0'})
    with opener.open(req,timeout=25) as response:page=response.read(3000000).decode('utf-8',errors='replace')
    links=[html.unescape(u) for u in re.findall(r'https://[^\s\"<>]+?\.exe',page) if 'nvidia_app' in u.lower()]
    link=next((u for u in links if nvidia_url(u)),None)
    if not link:raise OSError('Automatic download unavailable; use Official site below.')
    return link


def download_nvidia(destination,cancel,progress,link=None):
    link=link or nvidia_link()
    if not nvidia_url(link):raise ValueError('Invalid NVIDIA download source')
    opener=build_opener(NvidiaRedirect())
    target=Path(destination)/'nvidia';target.mkdir(parents=True,exist_ok=True)
    final=target/'NVIDIA-App-Setup.exe';partial=target/'NVIDIA-App-Setup.exe.part'
    try:
        with opener.open(Request(link,headers={'User-Agent':'PerfHub App Starter/1.0'}),timeout=30) as response,partial.open('wb') as out:
            if 'text/html' in response.headers.get('Content-Type','').lower():raise OSError('Server returned a web page instead of an installer')
            total=int(response.headers.get('Content-Length') or 0);received=0;last=0
            while True:
                if cancel.is_set():raise InterruptedError('Download stopped')
                chunk=response.read(262144)
                if not chunk:break
                out.write(chunk);received+=len(chunk)
                if received>1500000000:raise OSError('Unexpected installer size')
                if time.monotonic()-last>0.5:
                    progress(f'Downloading {received//1048576} MB'+(f' / {total//1048576} MB' if total else ''));last=time.monotonic()
        # Do not run a direct download unless Windows verifies its publisher signature.
        script="$s=Get-AuthenticodeSignature -LiteralPath $env:PERFHUB_INSTALLER_PATH; if($s.Status -eq 'Valid' -and $s.SignerCertificate.Subject -match 'NVIDIA'){exit 0}else{exit 1}"
        check=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],env={**os.environ,'PERFHUB_INSTALLER_PATH':str(partial)},capture_output=True,timeout=45,creationflags=0x08000000)
        if check.returncode:raise OSError('NVIDIA publisher signature could not be verified; use Official site.')
        partial.replace(final);return final
    finally:
        if partial.exists():partial.unlink()


class Runner:
    def __init__(self,events,destination,enable_ai=True):
        self.events=events;self.enable_ai=enable_ai;self.destination=Path(destination);self.stop=threading.Event();self.busy=False
    def start(self,keys,mode):
        keys=list(dict.fromkeys(keys))
        if self.busy or not keys:return False
        if mode not in ('download','install') or any(k not in APPS for k in keys):raise ValueError('Invalid app selection')
        self.stop.clear();self.busy=True
        threading.Thread(target=self.work,args=(keys,mode),daemon=True).start();return True
    def work(self,keys,mode):
        results=[];executable=winget_path()
        try:
            self.destination.mkdir(parents=True,exist_ok=True)
            from app_sources import latest_plan
            plan=latest_plan(keys,executable,self.stop,self.events.put,self.enable_ai)
            for index,key in enumerate(keys,1):
                if self.stop.is_set():break
                self.events.put(('status',key,f'{index}/{len(keys)} • '+('Downloading…' if mode=='download' else 'Installing…')))
                try:
                    if key=='nvidia':
                        path=download_nvidia(self.destination,self.stop,lambda value:self.events.put(('status',key,value)),link=plan.get(key,{}).get('url'))
                        if mode=='install':
                            os.startfile(str(path));status='Installer opened — complete NVIDIA setup'
                        else:status='Downloaded • publisher verified'
                    else:
                        if not executable:raise OSError('WinGet missing — use Get App Installer or Official site.')
                        if mode=='download':(self.destination/key).mkdir(parents=True,exist_ok=True)
                        args=command(executable,key,mode,self.destination)
                        version=plan.get(key,{}).get('version','')
                        if version and re.fullmatch(r'[A-Za-z0-9._+~-]{1,100}',version):args+=['--version',version]
                        # Drain output to a per-app log, avoiding pipe deadlocks on large installers.
                        log_dir=self.destination/'logs';log_dir.mkdir(exist_ok=True)
                        with (log_dir/(key+'.log')).open('w',encoding='utf-8') as log:
                            process=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
                            try:code=process.wait(timeout=1800)
                            except subprocess.TimeoutExpired:
                                process.terminate();process.wait(timeout=10);raise OSError('Timed out — check the log and retry.')
                        unsigned=code & 0xffffffff
                        if unsigned==0:status='Downloaded' if mode=='download' else 'Installed'
                        elif mode=='install' and unsigned==0x8A15002B:status='Already installed'
                        else:raise OSError(f'Needs attention ({unsigned:#x}) — open logs or Official site.')
                    results.append((key,True));self.events.put(('status',key,status))
                except Exception as exc:
                    results.append((key,False));self.events.put(('status',key,str(exc)[:230]))
        except Exception as exc:self.events.put(('error',str(exc)[:230]))
        finally:
            self.busy=False;self.events.put(('done',results,self.stop.is_set()))


DETAILS={
 'chrome':'Google’s web browser with profile sync, extensions and automatic updates.',
 'epic':'Install and manage games from the Epic Games Store. Epic account required for your library.',
 'discord':'Voice, video and text chat for communities and gaming. Discord account required.',
 'steam':'Valve’s game launcher, library and store. Steam account required.',
 'spotify':'Music and podcasts. Includes a free tier; some features require Premium.',
 'drive':'Sync files between Windows and Google Drive. Google account and cloud storage limits apply.',
 'nvidia':'Graphics settings, driver updates and recording for supported NVIDIA GPUs. Opens NVIDIA’s own setup when installing.',
 'afterburner':'GPU monitoring, fan control and optional tuning. Installing it does not apply an overclock.',
 'logitech':'Configuration for compatible Logitech gaming mice, keyboards and headsets.',
 'rgb':'Control supported RGB devices. Device support varies; some effects require a paid plan.',
 'capcut':'Video editing with effects, captions and export tools. Some features require an account or Pro.',
 'obs':'Free, open-source recording and streaming. Configure your scenes and outputs after installing.',
 'medal':'Record and share game clips. Account and optional subscription features are managed by Medal.'}


class AppStarterPage:
    def __init__(self,hub,tab,g,root):
        self.hub=hub;self.g=g;self.events=queue.Queue();self.closed=False;self.rows={};self.choices={};self.releases={};self.statuses={};self.expanded=set();self.checking=False;self.review_stop=threading.Event()
        self.destination=Path.home()/'Downloads'/'PerfHub Apps';self.runner=Runner(self.events,self.destination,enable_ai=hub.enable_ai)
        body=hub.page(tab,'App Starter','Open a package, review its apps, then install your selection here.')
        hub.label(body,'Install downloads and sets up the selected apps, or updates an existing version. Starting accepts their license agreements. Some vendor setups need your input.',10,g['MUTED'])
        toolbar=tk.Frame(body,bg=g['BG']);toolbar.pack(fill='x',padx=16,pady=8)
        self.mode=g['RSelect'](toolbar,['Install apps','Download installers'],width=220);self.mode.pack(side='left')
        g['RButton'](toolbar,'Open downloads',lambda:self.open_folder(self.destination)).pack(side='left',padx=8)
        g['RButton'](toolbar,'Open logs',lambda:self.open_folder(self.destination/'logs')).pack(side='left')
        hub.label(body,'CHOOSE A PACKAGE',11,g['ACC'])
        desc={'Everyday':'Browser, chat, music and files','Gaming':'Launchers, chat, music and clips','Creator':'Editing, streaming and file sync','Full setup':'All 13 apps, including device utilities'}
        self.buttons=[]
        for pair in (('Everyday','Gaming'),('Creator','Full setup')):
            line=tk.Frame(body,bg=g['BG']);line.pack(fill='x',pady=4)
            for name in pair:
                card=g['Card'](line);card.pack(side='left',fill='both',expand=True,padx=(0,10))
                hub.label(card.body,name,15);hub.label(card.body,desc[name],9,g['MUTED'])
                button=g['RButton'](card.body,'Review package',lambda n=name:self.preset(n));button.pack(anchor='w',padx=16,pady=(4,12));self.buttons.append((button,name))
        self.status=hub.label(body,'Choose a package to review it. Nothing installs until you press Install selected.',10,g['MUTED'])
        self.selection_title=hub.label(body,'All apps',18)
        actions=tk.Frame(body,bg=g['BG']);actions.pack(fill='x',padx=16,pady=8)
        self.start_button=g['RButton'](actions,'Install selected',self.start_selected,kind='primary');self.start_button.pack(side='left')
        self.check_button=g['RButton'](actions,'Check latest with AI',self.check_latest);self.check_button.pack(side='left',padx=8)
        self.stop_button=g['RButton'](actions,'Stop queue',self.stop);self.stop_button.pack(side='left')
        controls=tk.Frame(body,bg=g['BG']);controls.pack(fill='x',padx=16,pady=4)
        for label,callback in [('Add / browse all apps',self.browse_all),('Select shown',self.select_shown),('Clear selection',self.clear)]:g['RButton'](controls,label,callback).pack(side='left',padx=(0,8))
        self.count=hub.label(body,'0 apps selected',10,g['ACC'])
        hub.label(body,'AI checks current source information; WinGet resolves and verifies the actual installer. NVIDIA downloads use its official site and a publisher-signature check.',9,g['MUTED'])
        self.grid=tk.Frame(body,bg=g['BG']);self.grid.pack(fill='x',padx=(0,12))
        from branding import ASSETS
        self.logos={key:tk.PhotoImage(master=hub,file=str(ASSETS/'apps'/(key+'.png'))) for key in APPS}
        for key in APPS:self.choices[key]=tk.BooleanVar(value=False)
        self.visible=list(APPS);self.render_apps()
        hub.action(body,'Get Microsoft App Installer',lambda:hub.launch('https://apps.microsoft.com/detail/9nblggh4nns1'))
        self.mode.command=lambda *args:self.update_mode()
        hub.bind('<Destroy>',self.destroy,add='+');self.poll()
    def action_mode(self):return 'install' if self.mode.get()=='Install apps' else 'download'
    def update_mode(self):
        self.start_button.label=('Install' if self.action_mode()=='install' else 'Download')+' selected';self.start_button._draw()
    def update_count(self):self.count.config(text=f'{sum(v.get() for v in self.choices.values())} apps selected')
    def idle(self):return not self.runner.busy and not self.checking
    def lock(self,busy):
        self.start_button.set_enabled(not busy);self.check_button.set_enabled(not busy)
        for b,_ in self.buttons:b.set_enabled(not busy)
    def clear(self):
        if not self.idle():return
        for var in self.choices.values():var.set(False)
        self.update_count()
    def select_shown(self):
        if not self.idle():return
        for key in self.visible:self.choices[key].set(True)
        self.update_count()
    def browse_all(self):
        if not self.idle():return
        self.visible=list(APPS);self.selection_title.config(text='All apps — add to your selection');self.render_apps()
    def preset(self,name):
        if not self.idle():return
        for key,var in self.choices.items():var.set(key in PRESETS[name])
        self.visible=list(PRESETS[name]);self.selection_title.config(text=name+' package — select what you want')
        self.render_apps();self.update_count();self.status.config(text='Review app details or untick anything you do not want, then press Install selected.')
        if self.hub.enable_ai:self.check_latest()
    def render_apps(self):
        for child in self.grid.winfo_children():child.destroy()
        self.rows={};self.detail_labels={}
        for column in range(3):self.grid.columnconfigure(column,weight=1,uniform='apps')
        for i,key in enumerate(self.visible):
            _,name,category,package,website=APPS[key]
            card=self.g['Card'](self.grid);card.grid(row=i//3,column=i%3,sticky='nsew',padx=(0,8),pady=5)
            tk.Label(card.body,image=self.logos[key],bg=self.g['PANEL']).pack(pady=(14,3))
            label=self.hub.label(card.body,name,13);label.config(anchor='center',justify='center',wraplength=220)
            label=self.hub.label(card.body,category,9,self.g['MUTED']);label.config(anchor='center',justify='center',wraplength=220)
            self.g['RCheck'](card.body,'Include',self.choices[key],command=self.update_count).pack(pady=4)
            self.g['RButton'](card.body,'Hide details' if key in self.expanded else 'View details',lambda k=key:self.toggle_details(k)).pack(pady=4)
            status=self.hub.label(card.body,self.statuses.get(key,'Ready to check'),9,self.g['MUTED']);status.config(wraplength=220);self.rows[key]=status
            detail=self.hub.label(card.body,self.detail_text(key),9,self.g['MUTED']);detail.config(wraplength=220);self.detail_labels[key]=detail
            if key not in self.expanded:detail.pack_forget()
    def detail_text(self,key):
        record=self.releases.get(key,{})
        text=DETAILS[key]+'\n\nLatest: '+(record.get('version') or 'Resolved from the live source when you start.')
        text+='\nSource: '+record.get('source',APPS[key][3] or 'NVIDIA official download page')
        if record.get('ai'):text+='\nAI matched to current release evidence.'
        elif record:text+='\nSource checked; AI confirmation unavailable.'
        if record.get('url'):text+='\nDownload host: '+(urlsplit(record['url']).hostname or '')
        return text
    def toggle_details(self,key):
        if key in self.expanded:self.expanded.remove(key)
        else:self.expanded.add(key)
        self.render_apps()
    def check_latest(self):
        if not self.idle():return
        keys=[k for k,v in self.choices.items() if v.get()]
        if not keys:self.status.config(text='Select apps to check their latest releases.');return
        self.checking=True;self.review_stop.clear();self.lock(True);self.status.config(text='Checking current releases…')
        def work():
            try:
                from app_sources import latest_plan
                latest_plan(keys,winget_path(),self.review_stop,self.events.put,self.hub.enable_ai)
            finally:self.events.put(('checked',))
        threading.Thread(target=work,daemon=True).start()
    def start_selected(self):
        if not self.idle():return
        keys=[k for k,v in self.choices.items() if v.get()]
        if not keys:self.status.config(text='Select at least one app first.');return
        for key in keys:
            self.statuses[key]='Queued'
            if key in self.rows:self.rows[key].config(text='Queued')
        if self.runner.start(keys,self.action_mode()):self.status.config(text=f'Checking latest sources for {len(keys)} apps…');self.lock(True)
    def stop(self):
        if self.checking:self.review_stop.set();self.status.config(text='Stopping the release check…')
        if self.runner.busy:self.runner.stop.set();self.status.config(text='Stopping after the current app. Remaining apps will not start.')
    def open_folder(self,path):
        try:path.mkdir(parents=True,exist_ok=True);os.startfile(str(path))
        except OSError as exc:self.status.config(text=str(exc))
    def poll(self):
        if self.closed:return
        try:
            while True:
                event=self.events.get_nowait()
                if event[0]=='status':
                    self.statuses[event[1]]=event[2]
                    if event[1] in self.rows:self.rows[event[1]].config(text=event[2])
                    self.status.config(text=APPS[event[1]][1]+' • '+event[2])
                elif event[0]=='release':
                    self.releases[event[1]]=event[2]
                    text=('AI checked • ' if event[2].get('ai') else 'Source checked • ')+(event[2].get('version') or 'current installer')
                    self.statuses[event[1]]=text
                    if event[1] in self.rows:self.rows[event[1]].config(text=text)
                    if event[1] in self.detail_labels:self.detail_labels[event[1]].config(text=self.detail_text(event[1]))
                elif event[0] in ('error','phase'):self.status.config(text=event[1])
                elif event[0]=='checked':
                    self.checking=False;self.lock(False);self.status.config(text='Release check finished. Review the source details, then install your selection.')
                elif event[0]=='done':
                    ok=sum(success for _,success in event[1]);failed=len(event[1])-ok
                    self.status.config(text=f'{"Stopped" if event[2] else "Finished"}: {ok} completed, {failed} need attention.')
                    self.lock(False)
                    for key,text in list(self.statuses.items()):
                        if text=='Queued':
                            self.statuses[key]='Not started'
                            if key in self.rows:self.rows[key].config(text='Not started')
        except queue.Empty:pass
        self.job=self.hub.after(150,self.poll)
    def destroy(self,event):
        if event.widget is self.hub:
            self.closed=True;self.runner.stop.set();self.review_stop.set()
            if hasattr(self,'job'):
                try:self.hub.after_cancel(self.job)
                except tk.TclError:pass
