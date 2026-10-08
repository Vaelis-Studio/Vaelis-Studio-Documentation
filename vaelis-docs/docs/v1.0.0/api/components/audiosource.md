# AudioSource

> Vaelis 1.0.0 AudioSource component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/audiosource.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the AudioSource component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Audio Source; audio assets are under bottom Project → Audio and can be assigned to Audio Source.

## What it does

Play a local audio asset, optionally with distance-based 3D attenuation.

> **Component setup & editor tools:** AudioSource plays an imported audio asset from an entity.

## How to add and use AudioSource

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **AudioSource** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Audio Source. Assign an imported audio asset in the AudioSource section and use the script API for playback/state control.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `audioKey` | string|null | Audio asset key. | `null` |
| `is3D` | boolean | Enable distance attenuation. | `false` |
| `volume` | number | Volume 0-1. | `1` |
| `pitch` | number | Pitch multiplier; runtime API clamps to 0.25-4. | `1` |
| `loop` | boolean | Loop playback. | `true` |
| `autoplay` | boolean | Play automatically. | `true` |
| `minDistance` | number | Full-volume distance for 3D audio. | `100` |
| `maxDistance` | number | Silent distance for 3D audio. | `600` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `volume` | 0 silent; 1 the base configured level. |
| `pitch` | 1 normal playback speed; >1 faster/higher; <1 slower/lower. |
| `minDistance` | 3D only: inside this radius the source remains at full base volume. |
| `maxDistance` | 3D only: beyond this radius the source is silent. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `play()` | Method | Start/restart playback. |
| `playOnce()` | Method | Play without persistent looping. |
| `stop()` | Method | Stop playback. |
| `volume` | Property | Volume 0-1. |
| `pitch` | Property | Pitch multiplier. |
| `playing` | Property | Read-only playback state. |

## Examples

```
this.audio.playOnce();
```

```
this.audio.volume = 0.5;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
