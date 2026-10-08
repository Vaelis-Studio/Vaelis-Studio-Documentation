# SpriteAnimation

> Vaelis 1.0.0 SpriteAnimation component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/spriteanimation.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the SpriteAnimation component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Sprite Animation, then use the Animation editor window to create clips/import frames. The Animation editor is an editor window/modal, not the bottom Project panel.

## What it does

Sprite-sheet/clip animation state on a SpriteRenderer.

> **Component setup & editor tools:** SpriteAnimation stores clips and frames and is edited through the Animation Window.

## How to add and use SpriteAnimation

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **SpriteAnimation** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → SpriteAnimation → Open Animation Window. Create/edit clips, frames, FPS, looping, and playback there; use the Inspector for component-level playback state.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `clips` | array | Animation clip definitions. | `[]` |
| `currentClipId` | string|null | Current clip. | `null` |
| `playing` | boolean | Playback state. | `true` |
| `speed` | number | Playback speed multiplier. | `1` |
| `currentFrameIndex` | integer | Current frame index. | `0` |
| `frameElapsed` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `play(name)` | Method | Play an animation clip. |
| `stop()` | Method | Stop playback. |
| `playing` | Property | Read-only playback state. |
| `currentClip` | Property | Read-only current clip name. |
| `currentFrame` | Property | Current frame index. |
| `totalFrames` | Property | Read-only frame count. |
| `speed` | Property | Playback speed. |

## Examples

```
this.animator.play("Run");
```

```
this.animator.speed = 1.5;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
