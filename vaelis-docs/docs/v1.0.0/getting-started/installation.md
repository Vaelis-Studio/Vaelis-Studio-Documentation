# Installation

> Install and run the Vaelis portable distribution.

- Source: docs/v1.0.0/getting-started/installation.html
- Engine version: Vaelis 1.0.0

## How you actually use Vaelis

> **You do not have to install or self-host Vaelis to use it.:** The normal path is to visit the Vaelis website in a supported browser and use the editor online. Your browser runs the editor and game runtime. If you want the project/game available like an installed app, use the engine’s PWA/install option when available on your deployment.

| Method | When to use it | What you do |
| --- | --- | --- |
| **Use the website** | Normal users and beginners | Visit the deployed Vaelis website and open the editor. No local server or Node.js setup is required. |
| **Install the PWA** | You want an app-like shortcut/offline-capable experience supported by the deployment | Use the browser’s install/add-to-home-screen option when the site exposes it. The PWA is still the same web application; installation does not require running a local development server. |
| **Self-host** | You want to host Vaelis yourself—for example on your own web server, CodeSpaces/Codespaces, VS Code local development server, Vercel, or another static host | Use the local/server method below. This is an optional deployment/development method, not a prerequisite for ordinary use. |

## Self-hosting / local development

**The method below is only for people who want to host the engine themselves.** The supplied distribution is a static web application, so it can be served by a simple HTTP server. This is useful when developing the engine, modifying its source, testing local files, or deploying your own copy.

### Option A — simple local server

```
python3 -m http.server 5000
```

Run that command from the folder containing the Vaelis distribution, then open `http://localhost:5000/`. The browser must access the files through HTTP; opening the HTML file directly with `file://` can break module/WASM/network behavior.

### Option B — CodeSpaces / VS Code

Use a development server or forwarded port that serves the project directory over HTTP/HTTPS. The important requirement is not the editor you use—it is that the browser receives the static Vaelis files from a web origin.

### Option C — static hosting

Upload the distribution to a static host that serves JavaScript modules, JSON, WASM, assets, and the included routes. The supplied `vercel.json` contains route handling for Vercel-style hosting.

## Technical requirements

| Requirement | Detail |
| --- | --- |
| Browser | A modern browser capable of ES modules, WebAssembly, Canvas/WebGL as used by the runtime, and the browser APIs used by the editor. |
| Node.js | Not required to simply use the deployed editor or to serve the static client with Python. |
| Local HTTP server | Only required when you choose to self-host/preview locally. |
| Android APK export | Uses the separate build-server workflow described in the Android export documentation; the browser editor itself does not require an Android SDK. |

## Standalone builds

A standalone Vaelis game export contains `index.html`, `main.js` and `runtime/index.js`, built entirely client-side by the editor’s Export window. This export has no editor code in it and can be hosted anywhere that serves static files.

## Android APK

> **Requires a build server you provide:** The client distribution does not include an Android SDK, Gradle, or any local APK builder, and there is no bundled command-line exporter. Building an APK means sending your web export to an external build server you connect in the editor. See Android APK for the exact contract.
