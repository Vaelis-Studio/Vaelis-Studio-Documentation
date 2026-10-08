# StrokePath

> Vaelis 1.0.0 StrokePath component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/strokepath.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the StrokePath component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Top GameObject → 2D Object → Stroke Path. After a Stroke Path exists, the toolbar exposes Path (P); click empty space to append, drag points, and click segments to insert.

## What it does

A variable-thickness strip along placed points — rivers, cables, roads, conveyor belts or walls — with flat color or textured fill.

> **Component setup & editor tools:** StrokePath creates a drawable strip/path; its editing is performed with the Stroke Path viewport tool/gizmo.

## How to add and use StrokePath

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **StrokePath** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select an entity with StrokePath → use the Stroke Path viewport tool/gizmo to edit path points. Keep the Inspector open for serialized path/material settings.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `points` | array of {x,y} | Local-space point list defining the open polyline (not rotated/scaled by the Transform). | `[{x:-100,y:0}, {x:100,y:0}]` |
| `thickness` | number | Strip thickness. | `40` |
| `color` | hex string | Flat fill color, used when useTexture is false. | `#8a8a8a` |
| `opacity` | number | Opacity. | `1` |
| `useTexture` | boolean | Use an image texture along the path instead of a flat fill. | `false` |
| `textureKey` | string|null | Texture asset key. | `null` |
| `textureMode` | enum | stretch | tile. | `stretch` |
| `textureTiling` | number | Tiling length when textureMode is tile. | `100` |
| `textureScale` | number | Texture scale. | `1` |
| `textureOffset` | number | Texture offset; animatable for a flowing river/conveyor-belt look. | `0` |
| `textureFlip` | boolean | Flip texture. | `false` |
| `textureRotation` | number | Texture rotation. | `0` |
| `jointMode` | enum | Joint style between segments. | `round` |
| `capMode` | enum | End-cap style. | `round` |
| `smoothing` | number | 0-1. Runs the authored `points` through a Catmull-Rom spline resample BEFORE tessellation, turning the raw straight-segment polyline into a smooth curve — same idea as a… | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `thickness` | Larger values make the strip wider. |
| `textureTiling` | In TILE mode, larger values make each repeated texture cover more path length, so the image repeats less often. |
| `textureScale` | Higher scales the texture; lower makes it smaller/repeated more densely. |
| `textureOffset` | Changing this over time scrolls the texture along the path. |
| `opacity` | 0 invisible, 1 opaque. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `points` | Property | Local-space point array; reads return a fresh deep copy, writes replace the component’s array with a deep copy. |
| `thickness` | Property | Strip thickness. |
| `color` | Property | Flat fill color. |
| `opacity` | Property | Opacity. |
| `useTexture` | Property | Whether a texture is used instead of a flat fill. |
| `textureKey` | Property | Texture asset key. |
| `textureMode` | Property | stretch | tile. |
| `textureTiling` | Property | Tiling length. |
| `textureScale` | Property | Texture scale. |
| `textureOffset` | Property | Texture offset. |
| `textureFlip` | Property | Texture flip. |
| `getPoint(i)` | Method | Read one point by index. |
| `setPoint(i,x,y)` | Method | Overwrite one point. |
| `addPoint(x,y)` | Method | Append a point. |
| `insertPoint(i,x,y)` | Method | Insert a point at index i. |
| `removePoint(i)` | Method | Remove a point by index. |
| `pointCount` | Property | Read-only point count. |
| `getLength()` | Method | Total path length. |
| `firstPoint` | Property | Read-only first point. |
| `lastPoint` | Property | Read-only last point. |
| `worldToLocal(x,y)` | Method | Convert a world-space point to the entity’s local point space. |
| `localToWorld(x,y)` | Method | Convert a local-space point to world space. |
| `capMode` | Property | 'none' | 'box' | 'round' — see StrokePathCapMode in components/StrokePath.js. |
| `jointMode` | Property | 'sharp' | 'bevel' | 'round' — see StrokePathJointMode in components/StrokePath.js. |
| `textureRotation` | Property | Texture rotation in degrees, around each tile's own center. |

## Notes & behavior

- Points are placed with the Path tool in the Scene viewport, then adjusted by dragging a point or clicking a segment to insert a new one between two existing points.
- An open polyline (A to B), not a closed loop.
- Reads/writes on this.strokePath.points always operate on a copy, so mutating a returned array can never silently corrupt the live component; assign it back (or use the point methods) to apply a change.

## Examples

```
this.strokePath.addPoint(this.x, this.y);
```

```
this.strokePath.textureOffset += 20 * time.deltaTime; // flowing river/conveyor look
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
