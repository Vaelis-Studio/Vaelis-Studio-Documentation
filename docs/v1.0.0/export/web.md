# HTML5 & PWA

> Export Vaelis games as static web builds or installable PWAs.

- Source: docs/v1.0.0/export/web.html
- Engine version: Vaelis 1.0.0

## HTML5

HTML5 export produces a static site containing the game entry point and runtime assets. Serve it through an HTTP(S) server or upload it to a normal static host. Unused sprites and audio clips are not bundled, and assets are re-encoded (AVIF/WebP, Opus/WebM) where the exporting browser supports it.

## PWA

PWA export adds a web manifest and service worker so the game can install and run offline.

## Hosting checklist

- Serve the exported directory from a web server rather than opening the HTML with `file://` when ES modules or other browser security policies require HTTP.
- Keep the exported `runtime/` folder alongside the main game entry point.
- Use HTTPS in production when browser permissions, storage or installability require a secure context.
