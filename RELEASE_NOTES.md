PerfHub v1.4 — Audio Mixer, Storage Explorer & Monochrome Refresh

### What's new since v1.3

- Added **Audio Mixer** with per-application audio-session volume and mute controls across connected output devices.
- Added speaker and microphone volume/mute controls, device selection, and separate preferred devices for playback and calls.
- Added a resizable **pop-out mixer** with an optional **Always on top** setting. It stays synchronized with the mixer inside PerfHub.
- Added **Storage Explorer** with drive capacity, used/free space, file system, and utilization details.
- Added folder browsing, a path bar, Back/Up/Home navigation, file-name filtering, sortable file details, Copy path, and Show in File Explorer.
- Added Windows folder and file-type icons to Storage Explorer. Folder reads run in the background, and large listings load in batches.
- Refreshed the default Graphite theme with darker charcoal surfaces, white accents, a monochrome feather logo, rounded buttons, and a cleaner pill-shaped top bar.
- Updated the startup animation with a floating feather, orbiting lights, and a progress line.

### Fixes and improvements

- Replaced the buggy audio slider notch with a round thumb, reliable dragging, click-to-seek, and keyboard controls.
- Prevented audio refreshes from changing volume settings automatically or interrupting a drag.
- Made particle, firefly, and constellation animations fill the full panel width and adapt when resized.
- Fixed the packaged Pillow image-library mismatch that could prevent the program from starting.
- Preserved the existing tuning tools, Daily Tools, 100-app library, AI tools, and sidebar navigation.

### Getting Started

Close any older copy of PerfHub, then download and launch **PerfHub-v1.4.exe** below. No Python installation is needed.

Open **Audio Mixer** in the sidebar for volume/device controls, or **Storage** for the new explorer.

### Notes

- Volume, mute, and preferred-device changes apply immediately in Windows. Closing the mixer keeps the settings you selected.
- Apps appear in the mixer after creating an audio session. Windows sound settings remain available for additional driver-specific options.
- Storage browsing does not delete or modify files. Folder sizes are shown as a dash; file sizes appear in the listing.
- AI features and online downloads require an internet connection. Daily Tools continue processing files locally.
- Matching source files and artwork are included in **PerfHub-v1.4-source.zip**.

### Validation

Validated drive and audio-device/session discovery; storage browsing, filtering, sorting and scan cancellation; slider dragging and keyboard controls; mixer pop-out synchronization and refresh behavior; and packaged executable startup. The full 28-page application checks passed during this update. Audio write operations were tested with a fake backend to preserve the development PC's current audio settings.

---

# Daily Tools

- Added a Daily Tools sidebar tab with six locally processed utilities and no sign-in.
- Extract editable text from image files or clipboard images using Windows OCR; copy or save TXT.
- Batch-convert and proportionally resize images into PNG, JPEG, WebP, BMP and ICO.
- Build PDFs from ordered image lists, with page reorder/remove controls.
- Clean and transform text, format JSON, encode/decode URL/Base64, and undo changes.
- Calculate and compare SHA-256 file checksums.
- Sample original image pixels as HEX/RGB colors.
- Added opt-in keep-PerfHub-on-top and keep-PC/display-awake controls.
- Preserve originals and avoid filename collisions for image/PDF exports; run OCR/conversion/PDF/hashing off the UI thread.

Validation: generated-image OCR through the real Windows engine; all five export formats; alpha, orientation and metadata handling; collision-safe files; ordered PDF pages; checksums; text round trips/undo; all six UI dialogs and mocked power/window controls. Existing 100-app scrolling and full-app checks retained.

---

# App library scrolling fix

- Stabilize app-card heights while scrolling instead of sizing cards from temporary clipped child-window measurements.
- Keep details expanding and collapsing to their natural content height.
- Coalesce card sizing updates until layout has settled.

Validation: simulated clipped child sizes leave all 100 cards and the scroll range unchanged; repeated top/bottom scroll jumps, last-card details, search, selections and failure-help regression checks passed.

---

# Continuous app library and artwork

- Show all 100 apps on one scrollable page, with search and category filters.
- Bundle artwork for every app; images are available offline and scaled cleanly from 256px canvases.
- Reuse app cards when filtering and update details/failure help in place to avoid rebuilding the library.
- Keep selections across filters and setup packages, and select all matching apps with Select shown apps.
- Include artwork source metadata and third-party license notices.

Validation: continuous scrolling through the final card, search/categories, cached-card reuse, persistent selections, all 100 images, per-app error help and full app wiring checked without installing any apps.

---

# 100-app library and download failure help

- Expanded App Starter from 13 to 100 curated new-PC apps, with exact WinGet package IDs or the official NVIDIA download source.
- Added search, categories, 12-card pagination, persistent selections and additional setup bundles. Original bundles remain available.
- Added complete-installer checks so an empty download is not reported as successful; detect truncated NVIDIA downloads before publisher verification.
- Capture per-app error codes and bounded, redacted logs while continuing the remaining queue.
- Added a failed-app picker, Help fix this, optional AI explanations, local fallback guidance and deliberate retry controls.
- Keep download retries in download mode; AI advice never automatically executes a fix or substitutes download URLs.
- Bounded bulk AI source-review input and kept WinGet integrity checks and NVIDIA publisher checks in place.

Validation: 99 exact package identifiers checked against current WinGet metadata plus the NVIDIA official installer-link lookup. Simulated failure/success, privacy, AI fallback, pagination, selection persistence, full application navigation and sidebar tests passed. No applications were installed and no real AI requests were used in the regression tests.

---

# Navigation and embedded website fixes

- Changed sidebar animation to slide a fixed-width panel rather than relayout the entire page on each frame.
- Removed redundant tab remapping, navigation animations, and focus changes on repeated selections.
- Moved embedded browser startup and command writes off the main UI thread.
- Website tabs now navigate directly inside the application, avoiding iframe blocking and unnecessary iframe-to-page reloads.
- Added bounded automatic recovery for connection failures, HTTP errors, soft 404 pages, slow navigation, and native browser process crashes.
- Keep loaded browser pages and entered form values when changing tabs or toggling the sidebar.
- Ignore stale status events from closed browser instances.
- Display browser checks and rate limits without repeated automatic requests. Third-party site access rules still apply.

Validation: local WebView2 recovery fixtures, native process-crash recovery, 60 rapid tab/sidebar changes, non-blocking pipe checks, startup, page wiring, and embedded AI regression checks. Live BuildCores new-build navigation succeeded; PC Builds presented a Cloudflare browser check.

---

# Sidebar update

- The sidebar stays open when you select a tab. It only closes when you use the sidebar toggle or Ctrl+B.
- Added a quick slide animation for opening and closing the sidebar, replacing the previous fade.
- Rapid toggles reverse smoothly, and content expands into the available space.
- Existing pages, inputs, and embedded website layouts are preserved.

---

# PerfHub - PC Value Checker, 3D Builder & interface improvements

Changes since the supplied `PerfHub (1).exe` (the App Packages build).

## New features

- **PC Value Checker (Beta):** upload a PC photo and review its suggested components, enter parts manually, or use the hardware detected on the current PC.
- Choose a country and currency to estimate **new replacement value** and **used resale value**, with per-component ranges, totals, explanations, and source links where available.
- **3D PC Builder:** open BuildCores directly at its Create New Build page inside PerfHub.
- **Embedded bottleneck calculator:** use the existing PC Builds website inside the application, filling the available content area.
- **First-run desktop shortcut offer:** ask new users whether to create a desktop shortcut and remember their answer across later versions on that Windows account.

## Value Checker fixes and improvements

- Fixed keyboard focus so typing into component fields stays on the Value Checker page.
- Added a dedicated valuation request flow using the shared Gemini connection, with clearer service and quota error messages.
- Expanded price retrieval and fallback handling for components without matching current listings.
- Improved matching for component models, quantities, RAM kits, and individual storage drives.
- Keep two separate 1 TB drives separate instead of substituting two 2 TB drives; distinguish per-stick RAM capacity from total kit capacity.
- Added checks for mismatches between cited listing prices and displayed ranges. Unsupported references are removed or the result is labeled as an unverified estimate.
- Distinguish sourced listings, comparable replacements, and low-confidence AI estimates. Identify partial totals when prices are missing.

## Interface improvements

- Launch maximized while preserving the opening animation.
- Automatically collapse the sidebar after selecting a page to give tools more space.
- Added a clearer sidebar toggle, Show/Hide sidebar labels, a Ctrl+B shortcut, and quick fade transitions.
- Removed the extra bottleneck-page toolbar buttons so the website fills the content area while retaining PerfHub's surrounding controls.
- Added a Beta badge beside the PC Value Checker.
- Improved visibility and keyboard handoff when switching between native embedded pages and normal app inputs.

## Source publication

- Prepared a clean source folder with current Python and C# files, assets, build configuration, README, and a GPL-3.0 license for project-owned code.
- Included GeminiChat client source and integrated its compilation into the main build; third-party components keep their own terms.

## Notes

Valuations are estimates, not guaranteed sale prices. Some components may have only comparable or low-confidence estimates, or no available price. Online features depend on third-party availability, Gemini quota, and website restrictions. Embedded website tabs require Microsoft Edge WebView2 Runtime.
