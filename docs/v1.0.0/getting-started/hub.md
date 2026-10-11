# The Vaelis Hub

> Projects, starter templates, Learn and Installs tabs, offline PWA install and .vs file association.

- Source: docs/v1.0.0/getting-started/hub.html
- Engine version: Vaelis 1.0.0

## Overview

The Hub is the launcher page (`index.html` of the Vaelis site). Choose **Open Editor** or open a project card to enter the editor. A narrow icon rail on the left switches between three tabs.

| Tab | What it does |
| --- | --- |
| Projects | Recent projects with name, template and last-opened time. Click a card to open it, use the pencil to rename inline (Enter saves, Esc cancels) and the trash to remove it from the launcher. **New Project** opens the template picker. |
| Learn | Documentation entry point (quick start, scripting API, safety). Works offline because it is in the offline cache. |
| Installs | Shows the single engine build that ships with the Hub (Vaelis 1.0.0, Stable). |

## Starter templates

| Template | Contents |
| --- | --- |
| Blank Canvas | An empty environment for pure 2D rendering and custom logic (default). |
| Platformer Kit | Kinematic controller, one-way platforms and coyote-time jump tuning. |
| Top-Down | Playable starter with player, NPCs, collectible coins and a lit dungeon scene. |
| Flappy Bird | Complete flap-to-fly clone with state machine, scoring and juice, commented for beginners. |
| Sky Jumper | Endless cloud-hopping jumper with bouncy platforms, collectible stars, climbing camera and jump SFX. |
| Physics Sandbox | Rapier2D bodies, colliders and joints pre-wired for prototyping. |

Templates other than Blank Canvas are bundled real projects, applied the first time the new project opens in the editor.

## Install and offline use

1. Serve the client over HTTP(S) and open `/index.html` once while connected.
2. Wait for the first load to finish so the service worker can precache the editor, player, runtime and vendor files listed in `offline-manifest.json`.
3. Install the PWA from the browser. The editor, player and engine then launch without a network.

The service worker also serves the `/editor`, `/play` and `/player` aliases while offline. Android APK creation still needs the external build server. If the editor looks out of date after an update, reload once while online to refresh the cache.

## .vs project files

A `.vs` file is a ZIP archive with Vaelis's own extension. The web manifest declares a **file handler** for it. After installing Vaelis from Chrome or Edge, `.vs` files get the Vaelis icon (Windows, ChromeOS and Linux Chromium browsers), and double-click or **Open with → Vaelis** opens the editor with that project loaded as an unsaved session; use **File → Save Project** to write changes out. macOS and mobile browsers keep a generic icon.

For machines without the installed app, `file-association/` in the distribution has an optional Windows `.reg` file and a Linux install script. They set only the icon and type name, and are untested on real desktops.
