<div align="center">
  <h1>PerfHub</h1>
  <h3>Your PC. One control hub.</h3>
  <p>PC tools, hardware information, value estimates, and build planning<br>in one Windows desktop application.</p>
  <p><b>Windows desktop app &nbsp; · &nbsp; GPL-3.0 &nbsp; · &nbsp; PC Value Checker Beta</b></p>
  <p><a href="#easy-install-guide"><b>How to install</b></a> &nbsp; | &nbsp; <a href="https://perfhub-download.plumheron1.chatgpt.site/"><b>Visit the website</b></a> &nbsp; | &nbsp; <a href="#features"><b>Features</b></a></p>
</div>

---

## New in v1.4

- **Audio Mixer:** app volume and mute, speaker and microphone controls, preferred playback/call devices, and a synchronized pop-out with Always on top.
- **Storage Explorer:** drive usage, folder browsing, sortable file details, filtering, Windows file icons, and background folder reads.
- **Refreshed appearance:** charcoal and white Graphite theme, monochrome feather branding, rounder controls, and an animated startup screen.
- **Fixes:** smoother audio sliders, full-width particle animations, and corrected image-library packaging.

[Download PerfHub v1.4](https://github.com/cxeo22/Perf/releases/tag/v1.4) · [Changes since v1.3](https://github.com/cxeo22/Perf/releases/tag/v1.4)

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

Choose a tool from the sidebar. It stays open when you switch tabs. Click **Hide sidebar** or press **Ctrl+B** to slide it closed; use **Show sidebar** or **Ctrl+B** to slide it open again.

**That’s it. There is no separate installer to run after opening the EXE.** Keep the EXE in a folder where you want it to stay, especially if you create a shortcut to it.

<details>
<summary><b>Need help getting started?</b></summary>

- **Where is my download?** Open File Explorer and choose **Downloads**.
- **I downloaded a folder of code.** Go back to the release and download the file ending in `.exe` under **Assets**.
- **The website tabs do not load.** Install Microsoft Edge WebView2 Runtime if it is missing, then reopen PerfHub. The tabs open directly inside PerfHub and automatically retry temporary loading failures. Website browser checks and access restrictions can still require your attention.
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
  <tr><td><b>Drivers &amp; App Starter</b></td><td>Review driver support information and browse 100 curated apps with search, categories, setup bundles, and optional AI help for failed downloads or installs.</td></tr>
  <tr><td><b>Benchmark &amp; themes</b></td><td>Run a browser rendering benchmark and customize the application’s appearance.</td></tr>
</table>

### Before you use online tools

AI, live prices, and embedded websites need internet access. PC valuations are estimates, not guaranteed sale prices; some results use comparable parts or low-confidence estimates, and missing prices can produce partial totals. Review the component details and sources. Read proposed Windows changes before applying them.

See [release notes](RELEASE_NOTES.md) for the latest changes documented with this source package.

### App Starter: 100-app library

Browse 100 curated apps for setting up a new PC, including browsers, media tools, launchers, productivity apps, developer tools and hardware utilities. The collection is not a measured worldwide download ranking. See the [full app list and official sources](APP_LIBRARY.md).

Browse all 100 apps on one continuously scrolling page, with bundled app artwork. Search by name or filter by category; selections stay selected while filtering. The original setup packages remain available alongside New PC essentials, Developer and Creative tools bundles. Nothing is installed merely by browsing or selecting apps.

If a download or installation fails, the app records the return code and a redacted log excerpt. Choose the failed app from the failure picker or use **Help fix this** on its card. The help window provides local guidance, **Ask AI to explain**, an explicit retry button, and the official website. AI receives the app/error details and the displayed redacted log excerpt when requested; it does not automatically execute fixes. Local guidance remains available if AI is disabled or unavailable. Retry download does not silently switch to installation.

### Daily Tools

Open **Daily Tools** in the sidebar for these local utilities:

- **Image to text:** choose or paste a screenshot/photo, extract text, edit it, and copy it or save a UTF-8 TXT file. Uses Windows OCR and the installed Windows language support; no upload or AI key is needed. Review recognized text for mistakes.
- **Image converter & resizer:** batch-export PNG, JPEG, WebP, BMP or ICO, with optional maximum width/height. Proportions are preserved; images are not enlarged. ICO uses transparent square padding up to 256 pixels.
- **Images to PDF:** add up to 50 images, reorder the pages, and create a PDF. Each image becomes one page, with a 2400-pixel size limit for larger images.
- **Text toolbox:** trim, deduplicate or sort lines, remove blank lines, change case, format JSON, and encode/decode URLs or Base64. Includes Undo, Copy and Save TXT.
- **File checksum:** calculate SHA-256 and compare it with a publisher-provided value. A match verifies identical contents, not whether a file is safe.
- **Image color picker:** click an image preview to sample its corresponding original pixel and read RGB values or copy the HEX color.

Optional switches keep PerfHub on top or keep the PC/display awake while PerfHub remains open. Turning off keep-awake or closing PerfHub releases its sleep request. These tools do not require PowerToys.

Image/PDF exports use new filenames and do not overwrite originals. Transparency becomes white for JPEG, BMP and PDF; image exports omit source EXIF/GPS metadata. Animated inputs export their first frame. OCR requires an installed Windows OCR language (Windows Settings → Time & language → Language & region).

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

The script installs PyInstaller, Pillow, and pycaw, compiles GeminiChat and the other C# helpers, and packages:

```text
dist/PerfHub.exe
```

The packaged application requests administrator privileges when launched. The destination PC does not need Python installed.

### Run from Python

```bat
py -m pip install Pillow pycaw
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

Developer checks for Daily Tools: `check_daily_tools.py` uses Pillow and pypdf; `--ocr` also checks the real Windows OCR engine using generated images. `check_daily_tools_ui.py` uses mocked file dialogs and temporary generated files.
