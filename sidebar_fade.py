"""Quick, reversible sidebar fade. Covers only the sidebar, never the app."""
import time
import tkinter as tk

class SidebarFade:
    DURATION = .10
    def __init__(self, root, sidebar, colors, apply_layout):
        self.root, self.sidebar, self.colors, self.apply_layout = root, sidebar, colors, apply_layout
        self.overlay = None
        self.job = None
        self.closed = False

    def cancel(self):
        if self.job:
            try:self.root.after_cancel(self.job)
            except tk.TclError:pass
            self.job = None

    def transition(self, collapsed):
        self.cancel()
        if self.closed:return
        self.root.update_idletasks()
        if not self.root.winfo_viewable() or self.root.state() == 'iconic':
            self.finish(collapsed)
            return
        continuing = self.overlay is not None
        if not collapsed:self.apply_layout(False)
        self.root.update_idletasks()
        if not self.sidebar.winfo_ismapped():
            self.finish(collapsed)
            return
        try:
            if self.overlay is None:
                self.overlay = tk.Toplevel(self.root)
                self.overlay.withdraw()
                self.overlay.overrideredirect(True)
                self.overlay.transient(self.root)
                self.overlay.configure(bg=self.colors()['BG'])
                self.overlay.attributes('-alpha', 0 if collapsed else 1)
                self.overlay.attributes('-disabled', True)
            start = float(self.overlay.attributes('-alpha')) if continuing else (0 if collapsed else 1)
            target = 1 if collapsed else 0
            began = time.monotonic()
            def tick():
                if self.closed:return
                elapsed = min(1, (time.monotonic() - began) / self.DURATION)
                eased = elapsed * elapsed * (3 - 2 * elapsed)
                overlay = self.overlay
                overlay.configure(bg=self.colors()['BG'])
                overlay.geometry(f'{self.sidebar.winfo_width()}x{self.sidebar.winfo_height()}+{self.sidebar.winfo_rootx()}+{self.sidebar.winfo_rooty()}')
                overlay.attributes('-alpha', start + (target - start) * eased)
                overlay.deiconify();overlay.lift()
                if elapsed >= 1:self.finish(collapsed)
                else:self.job = self.root.after(12, tick)
            tick()
        except tk.TclError:
            self.finish(collapsed)

    def finish(self, collapsed):
        self.cancel()
        self.apply_layout(collapsed)
        if self.overlay is not None:
            try:self.overlay.destroy()
            except tk.TclError:pass
            self.overlay = None

    def close(self):
        self.closed = True
        self.cancel()
        if self.overlay is not None:
            try:self.overlay.destroy()
            except tk.TclError:pass
            self.overlay = None
