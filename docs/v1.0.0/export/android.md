# Android APK

> Build a debug-signed Android APK with the Vaelis APK service: use an API key in the editor, or export HTML5 and upload it on the service website.

- Source: docs/v1.0.0/export/android.html
- Engine version: Vaelis 1.0.0

> **The APK service:** APKs are built by the Vaelis APK service at https://apk-builder--vaelis-server.replit.app/ . The editor cannot compile APKs itself, and the client distribution contains no Android SDK or Gradle. The service is needed only while the APK is built; the finished APK runs on its own.

## Two ways to get your APK

### Option 1: use an API key in the editor

1. Get your API key for the APK service.
2. In the editor open **Export → Android APK** and click **+ Add build server**.
3. Enter a label (optional), the **Server URL** `https://apk-builder--vaelis-server.replit.app` and your **API Key**, then **Add server**.
4. Click the **Android APK** card. The editor builds your game, uploads it, shows progress and downloads the APK when it is ready.

### Option 2: no API key, export as HTML and upload on the website

1. In the editor choose **Export** and export as **HTML5** (PWA also works). A ZIP downloads.
2. Open <https://apk-builder--vaelis-server.replit.app/> in your browser.
3. Click **Upload** and choose the exported ZIP (the project export from step 1).
4. When the build finishes, download your APK.

> **Upload the exported game ZIP:** The ZIP must have index.html at its root. A saved project file ( .vs from File → Save Project) is not an export and will not build.

## Build behavior

- The server badge shows whether the service is awake. A sleeping free-tier host wakes when you build; the first attempt can time out, so retry.
- Use **Cancel build** in the Export window to stop a running job. Do not restart or close the editor mid-build.
- The server keeps a finished APK for about 30 minutes; the editor tells it to delete its copy as soon as the download is complete.
- The APK is debug-signed, suitable for installing and testing directly on a device.
- The game loads from the APK itself in a local WebView origin, so ES modules, JSON, audio, images and the physics WASM work with no server or internet at runtime. Pointer Events are preferred with Touch Events as a fallback.
- The favicon you choose in the Export window becomes the launcher icon.

## Request contract (for people running a build server)

The editor sends exactly this request, with the export ZIP as the body:

```
POST /api/v1/build?name=<url-encoded-game-title>
Content-Type: application/zip
X-Api-Key: <configured key>
```

- No other custom headers are sent; extra headers would fail the browser's CORS preflight. The server tells a standalone export apart by the ZIP contents (`index.html` at the root) and can read `manifest.webmanifest` and `sw.js` to tell PWA from plain HTML5.
- The response is a JSON job ticket with `statusUrl` (top level or under `job`). The completed status must provide `downloadUrl`. Relative URLs are resolved against the server URL.
- `GET /api/healthz` (CORS-enabled JSON) powers the awake badge.
- `DELETE <cancelUrl>` (from the ticket, falling back to `statusUrl`) cancels a job. It must be idempotent and the final status is `cancelled`, which the editor treats like `failed`. Status polling is also a heartbeat; a server should cancel jobs whose editor stops polling (about 60 seconds suggested).
- After a download the editor posts to the `/confirm-delivery` sibling of the download URL so the server can delete the APK early.
