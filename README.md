# PerfHub

Windows desktop hub for PC information, tuning tools, an AI assistant, a PC value checker, embedded bottleneck calculator, and BuildCores 3D PC Builder.

This folder contains the current application source and assets, without old application builds or local test profiles.

## Build on Windows

Install 64-bit Python with Tkinter and the Python launcher (`py`). Install Microsoft Edge WebView2 Runtime for the embedded website tabs. The build uses the Windows .NET Framework C# compiler at `%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe`.

Run `build_exe.bat` from this folder. It installs PyInstaller and Pillow, compiles the included C# hosts, and packages `dist/PerfHub.exe`. Internet access is needed to install Python dependencies. Launching the packaged application requests administrator privileges.

For development, install Pillow (`py -m pip install Pillow`) and run `py perfhub.py`. The bundled helper programs are required for AI and embedded browser features.

## Source layout

- `perfhub.py`, `hubplus.py`: application and pages
- Other Python modules: hardware inventory, value estimation, Windows tools, theming, and browser lifecycle
- `check_*.py`: development checks (read each check before running; some use live services)
- `ai/*.cs`: source for the native AI and browser hosts
- `ai/GeminiChat.cs`, `ai/build.ps1`: Gemini client source and standalone build script; the main build compiles this first
- `assets/`: application assets
- `renderbench.html`: browser rendering benchmark
- `PerfHub.spec`, `build_exe.bat`: executable build configuration

## Source availability and licensing

The GeminiChat client source is now included, and the build compiles all application-owned C# helpers from source. The shared Gemini credential is retained at the owner's request. AI operations require external Gemini service access and available quota.

The project-owned code is licensed under GNU GPL version 3 only (GPL-3.0-only). See [LICENSE](LICENSE) for the full terms. This license does not relicense third-party components or relicense third-party dependencies. Third-party components retain their own terms; WebView2 license and notice files are included in `ai/`. Confirm redistribution rights for supplied dependencies and assets.

## Upload to GitHub

Upload the CONTENTS of this folder to the repository root, not the folder itself. For a larger upload, GitHub Desktop can commit and push these contents. Put downloadable application EXEs in GitHub Releases instead of the source tree.
