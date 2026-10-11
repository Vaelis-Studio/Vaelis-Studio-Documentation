# Export overview

> Choose a Vaelis build target and understand the exported runtime package.

- Source: docs/v1.0.0/export/index.html
- Engine version: Vaelis 1.0.0

## Available targets

| Target | Status | Description |
| --- | --- | --- |
| HTML5 | Available | Static site: index.html + game files, built entirely client-side; upload to a web host or serve through HTTP. |
| PWA | Available | HTML5 plus manifest + service worker for installable/offline behavior. |
| Android APK | Available, through the APK service | Debug-signed APK. The editor cannot compile it locally: it POSTs your HTML5/PWA export to the Vaelis APK service, or you upload the HTML export on the service website. |
| Desktop Windows/Mac/Linux | Planned | Listed in the editor as coming soon. |

For every control in the Export window see [Export window reference](export-window.html). For Android, see [Android APK](android.html): use an API key, or export HTML5 and upload it at [the APK service](https://apk-builder--vaelis-server.replit.app/).

## Standalone game contract

The web export is a self-contained game package that includes `index.html`, `main.js` and the shipped runtime at `runtime/index.js`. It has no editor code in it — the same shape as the standalone target.

## Browser behavior

Pointer Events are used on modern platforms with raw Touch Events as a fallback. The runtime supports multi-touch, swipe, pinch, joystick and pen/stylus input.
