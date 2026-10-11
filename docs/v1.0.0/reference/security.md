# Security & play origin

> Scripts are not sandboxed. How the separate play origin works, what the editor protects, and what stays exposed.

- Source: docs/v1.0.0/reference/security.html
- Engine version: Vaelis 1.0.0

> **Game scripts are not sandboxed:** A project's scripts are compiled with new Function() and run as normal page code. Whatever origin the game runs on is what the script can reach. Only open projects from people you trust.

## Recommended setup: play on a separate origin

1. Deploy the **same folder** on a second hostname, for example `play.yourdomain.com` (on Vercel, add another domain to the same project).
2. In `project/editor/index.html` set `<meta name="vaelis-play-origin" content="https://play.yourdomain.com" />`.

Pressing Play then opens the game on the play origin and the editor sends the scene with `postMessage`. Scripts there cannot read the editor's `localStorage`, IndexedDB (saved projects, Android build server keys) or DOM, because browsers keep each origin's data apart.

- **Empty meta tag** keeps same-origin play. Fine for a private, local setup; not fine once you share projects.
- **Offline:** the other host cannot be reached, so the editor falls back to same-origin play and logs a warning.
- **`save` data** from Play lives on the play origin, separate from the editor's.
- Use `https://` in production and put nothing private (login cookies, editor data) on the play origin.

## What is protected

- **Message handling:** the editor accepts messages only from the play window it opened, on the origin it opened it on. The play window accepts messages only from the editor.
- **Escaped Console:** script output is escaped, so `console.log("<img onerror=...>")` cannot run code in the editor.
- **Escaped project data:** entity, script, tag and asset names come from project files and are escaped in the Hierarchy, Inspector, dropdowns and asset grid.
- **Shadowed globals:** inside a script, `window`, `document`, `globalThis`, `self`, `top`, `parent`, `frames`, `opener`, `open`, `localStorage`, `sessionStorage`, `indexedDB`, `caches`, `fetch`, `XMLHttpRequest`, `WebSocket` and `Function` are `undefined`. This stops accidents and one-line snooping only; the separate origin is the real protection. Use `save` and `global` instead of browser storage.
- **Import prompt:** loading a project that contains scripts asks for confirmation first.
- **No secrets shipped:** Android build server URLs and API keys are typed by the user and stored only in that browser's `localStorage`.

## What is still exposed

- In same-origin mode, everything a page on that origin can reach, including saved projects and build keys.
- A script can still make network requests from the play origin and affect its own game window. That is the nature of running someone's code.

## Third-party licenses

Vaelis bundles open-source libraries; see `THIRD_PARTY_LICENSES.md` in the distribution. Exported games include `THIRD_PARTY_LICENSES.txt`. Keep it in the folder when you publish.
