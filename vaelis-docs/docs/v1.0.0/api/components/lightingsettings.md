# LightingSettings

> Vaelis 1.0.0 LightingSettings component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/lightingsettings.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the LightingSettings component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Lighting Settings. This is scene-wide; one entity carrying the component supplies quality/mood values to the LightingSystem.

## What it does

Scene-wide lighting quality and mood controls. Attach to one entity; the lighting system reads it scene-wide.

> **Component setup & editor tools:** LightingSettings configures scene/entity lighting quality and ambient/shadow parameters used by the lighting system.

## How to add and use LightingSettings

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **LightingSettings** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Lighting Settings. Adjust quality/ambient/shadow parameters and verify changes with an active Light/ShadowCaster setup.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `shadowMode` | enum | quad | raymarch. | `quad` |
| `raymarchSteps` | number | 1-200 raymarch steps; only used in raymarch mode. | `24` |
| `ambientDarkness` | number | 0-1 darkness in unlit areas. | `0.65` |
| `glowStrength` | number | Visible light glow strength. | `1` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `ambientDarkness` | 0 leaves the unlit world bright; increasing toward 1 makes unlit areas darker. |
| `glowStrength` | Higher makes open-air light glow more strongly; 0 removes visible glow. |
| `raymarchSteps` | Higher improves raymarch shadow sampling but costs more GPU work; lower is cheaper but less detailed. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `shadowMode` | Property | quad | raymarch. |
| `raymarchSteps` | Property | Raymarch sample count 1-200. |
| `ambientDarkness` | Property | 0 = no darkening; 1 = darkest unlit areas. |
| `glowStrength` | Property | Visible light glow strength. |

## Examples

```
scene.lighting.shadowMode = "raymarch";
```

```
scene.lighting.raymarchSteps = 48;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
