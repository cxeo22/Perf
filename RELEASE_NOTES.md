# PerfHub â€” PC Value Checker, 3D Builder & interface improvements

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
