# Android APK

> Build a debug-signed Android APK by sending your web export to a build server you connect yourself.

- Source: docs/v1.0.0/export/android.html
- Engine version: Vaelis 1.0.0

## Requirements

> **This is not a local build:** The Vaelis client distribution does not include an Android SDK, Gradle, Java tooling, or any local/command-line APK builder. Android builds run on a server you connect; the editor itself cannot compile APKs.

## What you need

An Android build server URL and API key, from whoever operates that build service. Add them in **Export → Android APK** before building.

## Editor export

Use **Export → Android APK**, add or select a configured build server, then export. The editor builds the same HTML5/PWA package described in HTML5 & PWA and POSTs that exact ZIP to the server; the resulting APK is debug-signed for direct installation/testing.

## Request contract

For anyone operating a compatible build server: the editor sends `POST /api/v1/build?name=<title>` with the export ZIP as the body, headers `Content-Type: application/zip`, `X-Api-Key`, `X-ZenEngine-Standalone-Export: 1` and `X-ZenEngine-Export-Format: html|pwa`. The ZIP must contain `index.html` at its root. The server is expected to return a JSON job ticket with a `statusUrl`, and the completed status should include a `downloadUrl`.

## Runtime behavior

The finished APK hosts the game inside a local HTTPS-style WebView asset origin so ES modules, JSON, audio, images and the physics WASM runtime can work, and does not need the build server (or any other external URL) at runtime — only while it is being built. Modern Pointer Events are preferred, with Touch Events fallback.

## Launcher icon

When a favicon is selected in the export dialog, it is used as the Android launcher/app thumbnail icon.
