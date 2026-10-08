# ShadowCaster

> Vaelis 1.0.0 ShadowCaster component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/shadowcaster.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the ShadowCaster component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Shadow Caster. Enable it on objects that should occlude light; pair with a Light whose Cast Shadows is enabled.

## What it does

Marks an entity as a shadow occluder for the lighting system.

> **Component setup & editor tools:** ShadowCaster defines geometry that participates in the lighting/shadow system.

## How to add and use ShadowCaster

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **ShadowCaster** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Shadow Caster. Configure its serialized geometry in the Inspector and verify shadows in the viewport/game preview with a Light configured to cast shadows.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `enabled` | boolean | Enable shadow casting. | `true` |
| `width` | number|null | Shadow source width; null can derive from visual bounds. | `null` |
| `height` | number|null | Shadow source height; null can derive from visual bounds. | `null` |
| `offsetX` | number | Shadow offset X. | `0` |
| `offsetY` | number | Shadow offset Y. | `0` |
| `opacity` | number | Shadow opacity. | `1` |
| `length` | number | Shadow length multiplier. | `1` |
| `softness` | number | Shadow softness. | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `opacity` | 0 contributes no visible shadow; 1 is full caster contribution. |
| `length` | 1 uses the light’s natural reach; 0.5 makes a shorter shadow; 2 makes it reach twice as far. |
| `softness` | 0 is a crisp edge; increasing it broadens the penumbra. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `enabled` | Property | Enable shadow casting. |
| `width` | Property | Explicit caster width. |
| `height` | Property | Explicit caster height. |
| `offsetX` | Property | X offset. |
| `offsetY` | Property | Y offset. |
| `opacity` | Property | Shadow opacity. |
| `length` | Property | Shadow length. |
| `softness` | Property | Shadow softness. |

## Examples

```
this.shadowCaster.length = 2;
```

```
this.shadowCaster.softness = 0.25;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
