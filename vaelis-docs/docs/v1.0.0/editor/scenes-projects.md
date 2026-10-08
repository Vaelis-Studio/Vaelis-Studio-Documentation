# Scenes & projects

> Save, load, switch, duplicate and serialize Vaelis scenes and project manifests.

- Source: docs/v1.0.0/editor/scenes-projects.html
- Engine version: Vaelis 1.0.0

> **Exact control path:** Project-level scene/file operations are in the bottom Project panel. Scene creation uses Project → Scenes → New Scene ; Save Project and Load Project are in the top File menu. The autosave indicator/action is also exposed through File → Save Now / Saved .

## Scene workflow

The Scene Manager supports creating, saving, switching, renaming, duplicating and deleting scenes. The last remaining scene cannot be deleted.

## Project versioning

Saved projects are stamped with the engine version. The editor compares an incoming project manifest version with the current engine version and warns when a project was saved by a newer engine.

## Recommended practice

Keep source projects with explicit scene names, tags and stable IDs. Treat the serialized format as versioned data; do not silently reinterpret old scene JSON when a breaking engine change is introduced.
