"""Shared feather artwork for window, sidebar and startup branding."""
import sys
from pathlib import Path
import tkinter as tk
ASSETS=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))/'assets'
def feather(master,size=48,frame=None):
    name=f'feather-{size}.png' if frame is None else f'feather-fade-{frame}.png'
    return tk.PhotoImage(master=master,file=str(ASSETS/name))
def window_icon(root):
    if sys.platform=='win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PerfHub.Desktop.Feather')
    root._brand_icons=[feather(root,n) for n in (16,32,48,256)]
    root.iconphoto(True,*root._brand_icons)
