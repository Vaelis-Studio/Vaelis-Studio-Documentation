# Collider2D

> Vaelis 1.0.0 Collider2D component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/collider2d.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the Collider2D component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Collider 2D. One-way platform, trigger, shape, friction, restitution, density, layer and mask settings live here.

## What it does

Physics collision shape and contact filtering. A Collider2D is also required for accurate pointer/touch hit tests.

> **Component setup & editor tools:** Collider2D defines the collision/trigger shape used by the physics system.

## How to add and use Collider2D

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **Collider2D** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Collider 2D. After adding it, edit Shape, dimensions, Offset, Trigger, Friction, Restitution, Density, Layer, and Mask in the Collider2D section. The viewport Collider gizmo shows the collision shape.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `shape` | enum | Box | Circle | Capsule | Triangle. | `Box` |
| `width` | number | Box width. | `1` |
| `height` | number | Box height. | `1` |
| `radius` | number | Circle radius. | `0.5` |
| `capsuleHalfHeight` | number | Capsule half-height. | `0.5` |
| `capsuleRadius` | number | Capsule radius. | `0.3` |
| `trianglePoints` | 3 points | Triangle vertices in local space. | `[{x:-0.5,y:0.5}, {x:0.5,y:0.5}, {x:0,y:-0.5}]` |
| `offsetX` | number | Local X offset. | `0` |
| `offsetY` | number | Local Y offset. | `0` |
| `isTrigger` | boolean | Trigger-only collider. | `false` |
| `isOneWayPlatform` | boolean | One-way platform behavior. | `false` |
| `friction` | number | Surface friction. | `0.5` |
| `restitution` | number | Bounciness. | `0` |
| `density` | number | Density. | `1` |
| `layer` | 0-15 | Collision layer. | `0` |
| `mask` | 16-bit mask | Layers this collider can interact with. | `0xFFFF` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `restitution` | 0 behaves as non-bouncy; increasing it produces more bounce. Keep in a physically sensible range for predictable results. |
| `friction` | Higher values resist sliding more strongly. Lower values let contacts slide more easily. |
| `density` | Affects mass/inertia when the physics world builds the body from colliders; it is not a direct “heaviness” multiplier on gravity. |
| `offsetX / offsetY` | Moves the collider relative to the entity’s pivot; positive X/right and positive Y/down in world-space convention. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `shape` | Property | Box | Circle | Capsule | Triangle. |
| `width` | Property | Box width. |
| `height` | Property | Box height. |
| `radius` | Property | Circle radius. |
| `capsuleHalfHeight` | Property | Capsule half-height. |
| `capsuleRadius` | Property | Capsule radius. |
| `offset` | Property | {x,y} collider offset. |
| `isTrigger` | Property | Trigger-only collider. |
| `isOneWayPlatform` | Property | One-way platform flag. |
| `friction` | Property | Friction. |
| `restitution` | Property | Restitution. |
| `density` | Property | Density. |
| `layer` | Property | Layer index 0-15. |
| `mask` | Property | 16-bit interaction mask. |
| `isColliding` | Property | Read-only contact state. |

## Notes & behavior

- Collision layers use 16 membership layers (0-15). The mask determines which layers the collider can interact with.
- One-way platforms are intended to block from one side while allowing traversal from the non-blocking side.

## Examples

```
this.collider.isTrigger = true;
```

```
this.collider.layer = 2;
```

```
this.collider.mask = 0xFFFF;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
