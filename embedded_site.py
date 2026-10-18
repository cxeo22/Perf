"""Native browser lifecycle for the bottleneck tab; no AI or hardware upload."""
import json
from pathlib import Path
import subprocess
import threading
from embedded_ai import EmbeddedAI

URL = 'https://pc-builds.com/bottleneck-calculator/'

class EmbeddedSite(EmbeddedAI):
    def __init__(self, parent, colors, events, offline_test=False, builder=False):
        super().__init__(parent, colors, events, offline_test=offline_test)
        self.builder = builder
        self.event_name = 'builder_event' if builder else 'site_event'

    def start(self):
        if self.closed or (self.process is not None and self.process.poll() is None):
            return
        folder = Path(__file__).with_name('ai')
        try:
            args = [str(folder / 'EmbeddedSite.exe'), str(self.parent.winfo_id())]
            if self.offline_test:
                args += ['--offline-test', str(Path(__file__).with_name('verification') / ('webview-builder-profile' if self.builder else 'webview-profile'))]
            self.process = subprocess.Popen(args, cwd=str(folder), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            stderr=subprocess.DEVNULL, text=True, encoding='utf-8', bufsize=1, creationflags=0x08000000)
            self.send({'op':'theme', 'builder':self.builder, **self.colors()})
        except OSError:
            self.events.put((self.event_name, {'type':'error', 'message':'The embedded browser could not start. Switch tabs and reopen this tab to retry.'}))
            return
        process = self.process
        def read():
            try:
                for raw in process.stdout:
                    try:
                        data = json.loads(raw)
                    except ValueError:
                        continue
                    if isinstance(data, dict):
                        self.events.put((self.event_name, data))
            except (OSError, ValueError):
                pass
        threading.Thread(target=read, daemon=True).start()
