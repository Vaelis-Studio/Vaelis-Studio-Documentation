# Changelog

> Release notes and documentation scope for Vaelis 1.0.0.

- Source: docs/v1.0.0/reference/changelog.html
- Engine version: Vaelis 1.0.0

## 1.0.0 documentation baseline

This documentation snapshot reflects the portable Vaelis distribution provided with the request. It captures the public runtime API, component serialization model, editor surfaces, export targets and recent engine behaviors implemented in the distribution.

## Recent engine areas represented

The source includes rope/spring visual/physics refinements, Swing physics fixes, one-way platform collision work, lighting/shadow pipeline improvements, scripting autocomplete exposure and export/runtime file fixes. This documentation describes the resulting public surfaces without treating internal implementation notes as separate APIs.

## Documentation policy

When future versions ship, add release-specific API/reference pages and preserve the previous version. Breaking serialized-format changes belong in a new MAJOR version; compatible API additions can be MINOR releases.

## Corrections in this edition

This edition corrects the Android export documentation: earlier drafts described a local Gradle wrapper, an auto-downloaded Android SDK, a Java 17 requirement and a bundled `export-apk.js` command-line tool, none of which exist in the distribution. Android APK builds require an external, user-connected build server; see Android APK and the distribution README for the corrected description. It also adds the StrokePath component reference, the per-body-type this reference, several granular scripting pages, and the engine’s internal architecture rules — none of which change existing script-facing APIs.

## Documentation corrections (site redesign)

This edition of the documentation was re-verified against the client distribution source. Corrections:

- Android build-server request headers are `X-ZenEngine-Standalone-Export` and `X-ZenEngine-Export-Format` (previously documented with a `Vaelis` prefix).
- The Erase tool (Y) appears when a Tilemap or a Nav World 2D exists; a Tileset alone does not enable it.
- Added the editor’s Delete, copy/paste/duplicate, undo/redo and Space play shortcuts.
- Component field tables now list every serialized field with its source default (for example StrokePath defaults: thickness 40, colour `#8a8a8a`, round joints and caps, texture mode `stretch`). Engine-managed runtime fields are labelled as such.
- Script API tables now include members previously missing, such as `this.ear.canHear()` / `sourcesInRange`, `this.camera.x`/`y`, Rigidbody slope/wall angle limits, StrokePath `jointMode`/`capMode`/`textureRotation`, and the remaining Joystick styling members. `this.transform.scale` is an `{x, y}` object.
