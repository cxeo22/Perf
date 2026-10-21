@echo off
setlocal
cd /d "%~dp0"
title Build PerfHub EXE

echo ==========================================
echo         PerfHub EXE Builder
echo ==========================================
echo.
where py >nul 2>&1
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3 for Windows from https://www.python.org/downloads/
  echo During installation, enable "Add python.exe to PATH".
  pause
  exit /b 1
)

echo Installing/updating PyInstaller...
py -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo PyInstaller installation failed.
  pause
  exit /b 1
)

echo.
echo Building a single-file Windows executable...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ai\build.ps1
if errorlevel 1 exit /b 1
py -m pip install Pillow pycaw
if errorlevel 1 exit /b 1
"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:exe /platform:anycpu /out:ai\EmbeddedAI.exe /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll /reference:System.Net.Http.dll ai\EmbeddedAI.cs
if errorlevel 1 exit /b 1
"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:winexe /platform:anycpu /out:ai\DriverAI.exe /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll /reference:System.Net.Http.dll ai\DriverAI.cs
if errorlevel 1 exit /b 1
"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:exe /platform:anycpu /out:ai\ValueAI.exe /reference:System.Windows.Forms.dll /reference:System.Web.Extensions.dll /reference:System.Net.Http.dll ai\ValueAI.cs
if errorlevel 1 exit /b 1
"%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:exe /platform:x64 /out:ai\EmbeddedSite.exe /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll /reference:ai\Microsoft.Web.WebView2.Core.dll /reference:ai\Microsoft.Web.WebView2.WinForms.dll ai\EmbeddedSite.cs
if errorlevel 1 exit /b 1
py -m PyInstaller --clean --noconfirm PerfHub.spec
if errorlevel 1 (
  echo.
  echo Build failed. Read the error above.
  pause
  exit /b 1
)

echo.
echo SUCCESS: dist\PerfHub.exe
echo Copy only dist\PerfHub.exe to the PC where you want to use PerfHub.
echo The destination PC does not need Python installed.
pause
