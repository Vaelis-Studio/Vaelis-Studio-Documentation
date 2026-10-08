# AudioListener

> Vaelis 1.0.0 AudioListener component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/audiolistener.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the AudioListener component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Audio Listener. Usually keep one active listener in a scene for 3D hearing queries.

## What it does

Defines the hearing area for 3D audio and drives audio enter/leave callbacks.

> **Component setup & editor tools:** AudioListener defines the listening point used by positional audio behavior.

## How to add and use AudioListener

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **AudioListener** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Audio Listener. Use one intended listener for the active view; its radius/enabled settings control listening behavior.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `radius` | number | Hearing radius. | `300` |
| `enabled` | boolean | See the Inspector field of the same name. | `true` |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `radius` | Property | Listener radius. |
| `enabled` | Property | Enable/disable listener processing. |
| `canHear(…)` | Method | True if the named (or tagged, with {byTag:true}) 3D AudioSource entity is currently within range of this listener — the beginner-friendly single-target check, so a… |
| `sourcesInRange` | Property (read-only) | Every 3D AudioSource entity currently inside this listener's radius, as an array of live EntityContexts (empty array if none — never null, matches findAll()'s "always an… |

## Notes & behavior

- With an AudioListener present, scripts can receive onHearSound(source) and onLoseSound(source) transitions.

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
