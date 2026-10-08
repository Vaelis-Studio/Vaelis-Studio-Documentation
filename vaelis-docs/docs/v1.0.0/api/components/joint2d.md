# Joint2D

> Vaelis 1.0.0 Joint2D component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/joint2d.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the Joint2D component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Joint 2D; choose Fixed/Revolute/Prismatic/Rope/Spring and configure anchors/limits/motor.

## What it does

Connect physics bodies with Fixed, Revolute, Prismatic, Rope or Spring constraints.

> **Component setup & editor tools:** Joint2D constrains one physics body relative to another and requires compatible Rigidbody2D setup.

## How to add and use Joint2D

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **Joint2D** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Joint 2D. Configure the joint from its Inspector section and make sure the connected physics bodies satisfy the joint’s requirements.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `jointType` | enum | Fixed | Revolute | Prismatic | Rope | Spring. | `Revolute` |
| `connectedEntityId` | string|null | Entity ID of the connected body, or null for a world anchor. | `null` |
| `anchor1X` | number | Local anchor X on this entity. | `0` |
| `anchor1Y` | number | Local anchor Y on this entity. | `0` |
| `anchor2X` | number | Local anchor X on the connected body/world anchor. | `0` |
| `anchor2Y` | number | Local anchor Y on the connected body/world anchor. | `0` |
| `axisX` | number | Prismatic axis X. | `1` |
| `axisY` | number | Prismatic axis Y. | `0` |
| `length` | number | Rope maximum length or Spring rest length. | `100` |
| `stiffness` | number | Spring stiffness. | `6000` |
| `damping` | number | Spring damping. | `200` |
| `segmentCount` | integer | Rope/Spring visual/physical segments. | `18` |
| `ropeMass` | number | Mass per rope/spring segment. | `0.5` |
| `visualEnabled` | boolean | Enable visual joint rendering. | `true` |
| `visualColor` | hex string | Joint/rope visual color. | `#c8a66a` |
| `visualThickness` | number | Visual thickness. | `3` |
| `useTexture` | boolean | Use texture for rope-like visuals. | `false` |
| `textureKey` | string|null | Texture asset key. | `null` |
| `textureMode` | enum | stretch | tile. | `stretch` |
| `textureTiling` | number | Tiling length. | `32` |
| `textureScale` | number | Texture scale. | `1` |
| `textureOffset` | number | Texture offset. | `0` |
| `textureFlip` | boolean | Flip texture. | `false` |
| `limitsEnabled` | boolean | Enable joint angle/position limits where supported. | `false` |
| `limitMin` | number | Minimum limit. | `-45` |
| `limitMax` | number | Maximum limit. | `45` |
| `motorEnabled` | boolean | Enable motor. | `false` |
| `motorSpeed` | number | Motor target speed. | `0` |
| `motorMaxForce` | number | Maximum motor force. | `0` |
| `collideConnected` | boolean | Allow connected bodies to collide. | `false` |
| `enabled` | boolean | Enable the joint. | `true` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `length` | For Rope/Spring, higher length increases the rest/maximum link distance depending on the joint type. |
| `stiffness` | For Spring, higher values pull toward the rest length more strongly. |
| `damping` | Higher damping reduces oscillation faster. |
| `segmentCount` | Rope visual/solver subdivision count; higher can look smoother but costs more. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `jointType` | Property | Joint type. |
| `connectedEntity` | Property | Connected entity context, when one exists. |
| `anchor1` | Property | {x,y} local anchor on this body. |
| `anchor2` | Property | {x,y} local anchor on connected body/world anchor. |
| `axis` | Property | {x,y} prismatic axis. |
| `length` | Property | Joint length/rest length. |
| `stiffness` | Property | Spring stiffness. |
| `damping` | Property | Spring damping. |
| `segmentCount` | Property | Rope/spring segment count. |
| `ropeMass` | Property | Rope/spring segment mass. |
| `visualEnabled` | Property | Visual enabled. |
| `visualColor` | Property | Visual color. |
| `visualThickness` | Property | Visual thickness. |
| `useTexture` | Property | Use texture. |
| `textureKey` | Property | Texture asset key. |
| `textureMode` | Property | stretch | tile. |
| `textureTiling` | Property | Texture tiling. |
| `textureScale` | Property | Texture scale. |
| `textureOffset` | Property | Texture offset. |
| `textureFlip` | Property | Texture flip. |
| `limitsEnabled` | Property | Limits enabled. |
| `limitMin` | Property | Minimum limit. |
| `limitMax` | Property | Maximum limit. |
| `motorEnabled` | Property | Motor enabled. |
| `motorSpeed` | Property | Motor speed. |
| `motorMaxForce` | Property | Maximum motor force. |
| `collideConnected` | Property | Collision between connected bodies. |
| `enabled` | Property | Joint enabled. |

## Examples

```
this.joint.connectedEntity = findFirst("Target");
```

```
this.joint.jointType = "Spring";
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
