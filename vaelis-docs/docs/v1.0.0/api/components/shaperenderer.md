# ShapeRenderer

> Vaelis 1.0.0 ShapeRenderer component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/shaperenderer.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the ShapeRenderer component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Create directly from top GameObject → Shape → Square/Circle/Capsule/Triangle, or Inspector → Add Component → Shape Renderer.

## What it does

Draw a procedural 2D shape without requiring a sprite asset.

> **Component setup & editor tools:** Use ShapeRenderer when you want a procedural shape without importing an image.

## How to add and use ShapeRenderer

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **ShapeRenderer** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Inspector → ShapeRenderer: choose the shape type and edit its dimensions. For triangle/freeform shapes, the corresponding viewport gizmo is used when available.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `shapeType` | enum | Square, Circle, Triangle or Capsule. | `Square` |
| `width` | number | Square width. | `100` |
| `height` | number | Square height. | `100` |
| `radius` | number | Circle radius. | `50` |
| `capsuleHalfHeight` | number | Capsule half-height along its vertical axis. | `50` |
| `capsuleRadius` | number | Capsule cap radius. | `30` |
| `trianglePoints` | 3 points | Triangle vertices in local space. | `[{x:-50,y:50}, {x:50,y:50}, {x:0,y:-50}]` |
| `fillColor` | hex string | Fill color. | `#3a8ede` |
| `opacity` | number | Opacity. | `1` |
| `outlineEnabled` | boolean | Enable outline. | `false` |
| `outlineColor` | hex string | Outline color. | `#ffffff` |
| `outlineWidth` | number | Outline width. | `2` |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `shapeType` | Property | Square | Circle | Capsule | Triangle. |
| `width` | Property | Shape width. |
| `height` | Property | Shape height. |
| `radius` | Property | Circle radius. |
| `capsuleHalfHeight` | Property | Capsule half-height. |
| `capsuleRadius` | Property | Capsule radius. |
| `fillColor` | Property | Fill hex color. |
| `opacity` | Property | Opacity. |
| `outlineEnabled` | Property | Whether the outline is rendered. |
| `outlineColor` | Property | Outline hex color. |
| `outlineWidth` | Property | Outline width. |

## Examples

```
this.shape.fillColor = "#22c55e";
```

```
this.shape.shapeType = "Circle";
```

```
this.shape.radius = 32;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
