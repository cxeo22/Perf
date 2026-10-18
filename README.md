<div align="center">
  <img src="assets/feather-256.png" width="96" height="96" alt="PerfHub feather logo">
  <h1>PerfHub</h1>
  <h3>Your PC. One control hub.</h3>
  <p>Explore your hardware, review tuning options, estimate your PC’s value,<br>and plan your next build from one Windows desktop application.</p>
  <p>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square" alt="Platform: Windows">
    <img src="https://img.shields.io/badge/License-GPL--3.0-4c956c?style=flat-square" alt="License: GPL-3.0">
    <img src="https://img.shields.io/badge/PC_Value_Checker-Beta-d99a2b?style=flat-square" alt="PC Value Checker: Beta">
  </p>
  <p><a href="#download--run"><b>Download &amp; run</b></a> &nbsp; • &nbsp; <a href="#whats-inside"><b>Explore features</b></a> &nbsp; • &nbsp; <a href="#build-from-source"><b>Build from source</b></a></p>
</div>

---

## Download & run

**Just want to use PerfHub? Download the EXE from this repository’s Releases section. You do not need Python or any build tools.**

1. Open **Releases** on the repository’s main page and choose the latest release.
2. Under **Assets**, download the **PerfHub `.exe`**. The source ZIP is for developers.
3. Run the EXE and approve the Windows administrator prompt if you want to launch the application.
4. On your first launch, choose whether to create a desktop shortcut.

<table>
  <tr><th>For everyday users</th><th>For developers</th></tr>
  <tr><td>Download the release EXE and run it.</td><td>Download or clone the source and follow the build instructions below.</td></tr>
  <tr><td>No Python installation required.</td><td>Python and C# build tools are required.</td></tr>
</table>

**Requirements:** Windows; internet access for AI, live pricing, and external websites; Microsoft Edge WebView2 Runtime for embedded website tabs. WebView2 may already be installed. AI availability depends on the Gemini service and its quota.

## What’s inside

<table>
  <tr><th>Feature</th><th>What you can do</th></tr>
  <tr><td><b>PC Value Checker · Beta</b></td><td>Upload a photo, review or enter components, or use detected PC hardware. Choose a country and currency to see new replacement and used resale ranges, explanations, and sources where available.</td></tr>
  <tr><td><b>3D PC Builder</b></td><td>Open BuildCores directly at its Create New Build page inside PerfHub.</td></tr>
  <tr><td><b>Bottleneck calculator</b></td><td>Access the PC Builds calculator in an embedded tab with a full-size content area.</td></tr>
  <tr><td><b>AI assistant</b></td><td>Ask questions about your PC and PerfHub’s tools using the Gemini connection.</td></tr>
  <tr><td><b>Hardware &amp; monitoring</b></td><td>Review detected components, system information, and live CPU and RAM usage.</td></tr>
  <tr><td><b>Tuning &amp; Windows tools</b></td><td>Explore presets, individual tweaks, game profiles, storage tools, backups, and activity records.</td></tr>
  <tr><td><b>Drivers &amp; App Starter</b></td><td>Review driver support information and use selectable application packages.</td></tr>
  <tr><td><b>Benchmark &amp; customization</b></td><td>Run the browser rendering benchmark, change themes, and use the collapsible sidebar.</td></tr>
</table>

### A cleaner workspace

PerfHub starts maximized, preserves its opening animation, and collapses the sidebar when you select a page. Use the sidebar toggle or **Ctrl+B** to reopen it. Embedded pages fill the available content area.

### About the estimates

PC valuations are estimates rather than guaranteed sale prices. Results distinguish current listings, comparable replacements, and low-confidence AI estimates. Missing prices can produce partial totals. Confirm component details and review the linked sources before relying on an estimate. External websites may impose browser checks or other access restrictions.

Read [the release notes](RELEASE_NOTES.md) for the changes since the earlier App Packages build.

---

## Build from source

**This section is for developers. It is not required to use the release EXE.**

<details>
<summary><b>Expand developer setup and build instructions</b></summary>

### Prerequisites

- 64-bit Python with Tkinter and the Python launcher (`py`).
- Windows .NET Framework C# compiler at `%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe`.
- Microsoft Edge WebView2 Runtime to use the embedded website tabs.
- Internet access to install Python build dependencies.

### Build the executable

Run this from the source folder, or double-click the file:

```bat
build_exe.bat
```

The script installs PyInstaller and Pillow, compiles GeminiChat and the other C# helpers, and packages:

```text
dist/PerfHub.exe
```

The packaged application requests administrator privileges when launched. The destination PC does not need Python installed.

### Run from Python

```bat
py -m pip install Pillow
py perfhub.py
```

The helper programs in `ai/` are also required for AI and embedded browser features. Recompile them after changing their C# source.

### Source map

| Files | Purpose |
| --- | --- |
| `perfhub.py`, `hubplus.py` | Main application and pages |
| Other Python modules | Hardware inventory, valuation, Windows tools, themes, and browser lifecycle |
| `check_*.py` | Development checks; inspect each before running, since some use live services |
| `ai/*.cs` | Native AI client and helper source |
| `ai/build.ps1` | Standalone GeminiChat build script |
| `assets/` | Application artwork and icons |
| `renderbench.html` | Browser rendering benchmark |
| `PerfHub.spec`, `build_exe.bat` | Executable packaging and build configuration |

</details>

## Source & license

The GeminiChat source is included, and the main build compiles all application-owned C# helpers from source. The shared Gemini credential is retained at the owner’s request; AI operations require service access and available quota.

Project-owned code is licensed under **GNU GPL version 3 only (GPL-3.0-only)**. See [LICENSE](LICENSE) for the full terms. Third-party dependencies retain their own licenses; the WebView2 license and notices are in `ai/`.

<div align="center">
  <hr>
  <p><b>PerfHub</b><br>PC tools, component estimates, and build planning in one place.</p>
</div>
