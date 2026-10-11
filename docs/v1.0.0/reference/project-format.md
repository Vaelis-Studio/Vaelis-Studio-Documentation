# Project format

> Understand the engine-versioned project container and portable distribution layout.

- Source: docs/v1.0.0/reference/project-format.html
- Engine version: Vaelis 1.0.0

## Project version

Vaelis 1.0.0 stores the engine version in its runtime and launcher version constants. Saved manifests are stamped with that version so opening a project created by a newer engine can produce a compatibility warning.

## Distribution layout

| Path | Purpose |
| --- | --- |
| project/runtime/ | Engine runtime shipped with games. |
| project/editor/ | Development editor, including the HTML5/PWA exporter. |
| `project/player/` | Standalone standalone runtime shell. |
| project/vendor/ | Local third-party runtime/editor dependencies (Pixi, Rapier, Hammer, Monaco, JSZip). |
| css/, icons/, js/ | The engine hub client (project browser, new-project flow, templates). |
| sw.js, offline-manifest.json | Offline PWA support for the hub/editor itself. |

## What is not included

> **No local Android tooling:** This client distribution is intentionally static: it ships no Android SDK, Gradle, Java build scripts, Node server, or local APK builder. Android APKs are built by an external build server the person running the editor configures themselves — see Android APK.

## Runtime boundary

Runtime never imports editor modules. This keeps exported games independent from the editor and is one of the core architectural invariants of the distribution.
