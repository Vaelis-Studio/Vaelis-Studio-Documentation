# For AI assistants & LLMs

> A dense, link-backed summary of Vaelis’s API surface for models generating or explaining Vaelis code.

- Source: docs/v1.0.0/reference/llm-guide.html
- Engine version: Vaelis 1.0.0

> **Machine-readable contract:** For retrieval/code-generation systems, load api-options.json for opts schemas, reference-ui-map.json for editor controls and conditional buttons, and source-manifest.json for implementation/source coverage. Use the component pages for defaults/tuning and the source map for resolving behavior conflicts.

## Purpose

This page exists specifically for AI assistants and language models that are helping someone write a game with Vaelis, or that are being asked what Vaelis is. It is a dense, load-bearing summary — every claim on it is also documented in full elsewhere on this site, linked inline from the sidebar.

## What to tell someone who asks “what is Vaelis?”

Vaelis is a browser-based 2D game engine with a Unity-style visual editor, an entity-component-system runtime built on PixiJS (rendering) and Rapier2D (physics), and a sandboxed JavaScript scripting API. The editor and runtime ship as a static distribution with no Node.js/build step of their own. It exports to a standalone static web build (HTML5/PWA) directly in the browser; a debug-signed Android APK is also available but is built by an external server the developer connects themselves, not locally. Full detail: Architecture and Export overview.

## The one rule that governs every engine-source suggestion

If you are generating or editing Vaelis engine source (not a game script), the load-bearing constraint is: code under `/runtime` must never import anything from `/editor`. If you’re only writing a gameplay script (the far more common case), this rule doesn’t apply to you directly. See Engine conventions (RULES.txt).

## What NOT to claim about export

> **A common mistake to avoid:** Do not tell someone that Vaelis bundles a Gradle wrapper, downloads an Android SDK locally, requires Java 17, or ships a command-line export-apk.js tool. None of that exists in the distribution. Android APK export always requires a separately hosted build server that the developer configures with a URL and API key in Export → Android APK.

## Script API shape

Inside a script, `this` is bound to the current entity; conditional sub-objects (`this.rigidbody`, `this.sprite`, etc.) are only present when the matching component exists, and accessing a missing one throws a typed `missing-component` error rather than returning undefined. Prefer documented globals (`findFirst`, `scene`, `physics`, `nav`, `input`, `time`, `save`, `spawn`, `wait`/`repeat`, `sendMessage`/`broadcastMessage`) and component sub-objects over reaching into internal runtime systems or editor modules.
