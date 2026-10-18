# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['perfhub.py'],
    pathex=['.build-deps'],
    binaries=[],
    datas=[('assets', 'assets'), ('renderbench.html', '.'), ('ai/GeminiChat.exe', 'ai'), ('ai/EmbeddedAI.exe', 'ai'), ('ai/EmbeddedAI.exe.config', 'ai'), ('ai/DriverAI.exe', 'ai'), ('ai/ValueAI.exe', 'ai'), ('ai/ValueAI.exe.config', 'ai'), ('ai/EmbeddedSite.exe','ai'), ('ai/Microsoft.Web.WebView2.Core.dll','ai'), ('ai/Microsoft.Web.WebView2.WinForms.dll','ai'), ('ai/WebView2Loader.dll','ai'), ('ai/WebView2-LICENSE.txt','ai'), ('ai/WebView2-NOTICE.txt','ai')],
    hiddenimports=['perfdata', 'hubplus'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PerfHub',
    icon='assets/feather.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
