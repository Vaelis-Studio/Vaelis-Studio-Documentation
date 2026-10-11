# Export window reference

> Every control in the Export window: game title, favicon, formats, asset optimization, Android build servers, progress, cancel and results.

- Source: docs/v1.0.0/export/export-window.html
- Engine version: Vaelis 1.0.0

Open it from **File → Export…** or the toolbar **Export** button.

## Game details

| Field | Behavior |
| --- | --- |
| Game title | Up to 80 characters; defaults to the project name. Used as the page title and, for APKs, the app name. |
| Favicon (optional) | Choose any image; **Change…** and **Remove** manage it. Used as the page icon and the Android launcher icon. |

## Format cards

| Card | Status | Output |
| --- | --- | --- |
| HTML5 | Available | Static site: `index.html` plus game files. |
| PWA | Available | HTML5 plus manifest and service worker for install and offline play. |
| Desktop (Windows/Mac/Linux) | Coming soon (disabled) | Not built in 1.0.0. |
| Android APK | Available | One debug-signed APK built on a server. See [Android APK](android.html). |

## What the build does

- Runs entirely in the browser. Images are re-encoded to AVIF when the browser can encode it, otherwise WebP, otherwise left as is. Every candidate is decoded back to verify it before it is trusted. Audio becomes Opus in WebM when the browser can record it.
- Sprites and audio not referenced by any scene, prefab or script are left out.
- Assets are written as real binary files, never base64.
- No editor code is included. The game owns its own render loop and is not frame-capped.

## Result screen

After HTML5 or PWA export the download starts and the window shows how many images and audio clips were bundled, the size saved (before and after), and how many unused assets were skipped. A warning reminds you not to double-click `index.html`: from `file://` the game shows a blank page, so upload the folder to a static host (itch.io, GitHub Pages, Vercel, Netlify) or run a local server (`npx serve .`).

If an Android build server is saved, **Build APK from this HTML5 (or PWA) export** sends the export you just made without rebuilding. **Export another format** resets the window.

## Android build servers

Under the Android card you can save several servers (label, URL, API key), pick the active one, edit or remove entries. They are stored only in this browser. A badge shows *Checking server…*, *Server awake* or *Server may be asleep* (free hosts sleep after inactivity; building wakes them, but the first request can be slow or time out, so try again).

## Progress and cancel

Android builds show a **Cancel build** button. Do not restart or leave the editor while an APK builds; cancelling (or leaving) asks the server to stop the job. The editor polls the build every 2.5 seconds and gives up after 10 minutes. HTML5 and PWA exports finish locally and cannot be cancelled.
