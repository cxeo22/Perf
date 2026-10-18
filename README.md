<div align="center">
  <h1>PerfHub</h1>
  <h3>Your PC. One control hub.</h3>
  <p>PC tools, hardware information, value estimates, and build planning<br>in one Windows desktop application.</p>
  <p><b>Windows desktop app &nbsp; · &nbsp; GPL-3.0 &nbsp; · &nbsp; PC Value Checker Beta</b></p>
  <p><a href="#easy-install-guide"><b>How to install</b></a> &nbsp; | &nbsp; <a href="https://perfhub-download.plumheron1.chatgpt.site/"><b>Visit the website</b></a> &nbsp; | &nbsp; <a href="#features"><b>Features</b></a></p>
</div>

---

## Easy install guide

**You only need the PerfHub EXE. You do not need Python, source code, or developer tools.**

### 1. Download

On this repository’s main page, click **Releases**, then open the newest release. Under **Assets**, click the file ending in **`.exe`**.

Choose the **PerfHub EXE**, rather than **Source code (zip)** or **Source code (tar.gz)**.

### 2. Open

Wait for the download to finish. Open your **Downloads** folder and double-click the PerfHub EXE.

Windows will ask for administrator permission. Check that you are opening the PerfHub file you downloaded, then choose **Yes** to start it.

### 3. Choose your shortcut

The first time PerfHub runs, it asks whether you want a desktop shortcut. Choose **Yes** for easy access next time, or **No** to continue without one.

### 4. Start using PerfHub

Choose a tool from the sidebar. The sidebar closes to give the page more room; click **Show sidebar** or press **Ctrl+B** to open it again.

**That’s it. There is no separate installer to run after opening the EXE.** Keep the EXE in a folder where you want it to stay, especially if you create a shortcut to it.

<details>
<summary><b>Need help getting started?</b></summary>

- **Where is my download?** Open File Explorer and choose **Downloads**.
- **I downloaded a folder of code.** Go back to the release and download the file ending in `.exe` under **Assets**.
- **The website tabs do not load.** Install Microsoft Edge WebView2 Runtime if it is missing, then reopen PerfHub. Website browser checks and access restrictions may also affect loading.
- **AI or live pricing is unavailable.** Check your internet connection. These features also depend on external services and available Gemini quota.
- **Do I need Python?** No. Python is only needed if you want to work with the source code.

</details>

## PerfHub website

### [Visit the PerfHub website →](https://perfhub-download.plumheron1.chatgpt.site/)

The PerfHub website introduces the application, shows its main tools through interface previews and feature tours, and provides a Windows download button. Use it to learn what PerfHub does before downloading.

**The desktop app runs on your computer.** The website is a place to explore PerfHub and get the download; it does not apply Windows tweaks to your PC through your browser. For the newest published version, use this repository’s latest release.

## Features

<table>
  <tr><th>Tool</th><th>What it does</th></tr>
  <tr><td><b>PC Value Checker · Beta</b></td><td>Upload a PC photo, enter components, or use your detected hardware. Choose a country and currency to estimate new replacement and used resale value, with ranges, explanations, and sources where available.</td></tr>
  <tr><td><b>3D PC Builder</b></td><td>Open BuildCores at its Create New Build page inside PerfHub.</td></tr>
  <tr><td><b>Bottleneck calculator</b></td><td>Use the PC Builds website inside a full-size application tab.</td></tr>
  <tr><td><b>AI assistant</b></td><td>Ask about your PC and PerfHub’s tools through the Gemini connection.</td></tr>
  <tr><td><b>Hardware information</b></td><td>View detected components, system information, and live CPU and RAM usage.</td></tr>
  <tr><td><b>Tuning &amp; Windows tools</b></td><td>Review presets, individual tweaks, game profiles, storage tools, backups, and activity records.</td></tr>
  <tr><td><b>Drivers &amp; App Starter</b></td><td>Review driver support information and choose application packages.</td></tr>
  <tr><td><b>Benchmark &amp; themes</b></td><td>Run a browser rendering benchmark and customize the application’s appearance.</td></tr>
</table>

### Before you use online tools

AI, live prices, and embedded websites need internet access. PC valuations are estimates, not guaranteed sale prices; some results use comparable parts or low-confidence estimates, and missing prices can produce partial totals. Review the component details and sources. Read proposed Windows changes before applying them.

See [release notes](RELEASE_NOTES.md) for the latest changes documented with this source package.

## Open source

Project-owned code is licensed under **GNU GPL version 3 only (GPL-3.0-only)**. Read [LICENSE](LICENSE) for the full terms. Third-party components retain their own licenses; WebView2 license and notice files are included in `ai/`.

---

## For developers

**Regular users can skip this section. Downloading and running the release EXE is enough.**

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

The GeminiChat source is included, and the main build compiles the application-owned C# helpers. The shared Gemini credential is retained at the owner’s request; service access and quota still apply.
