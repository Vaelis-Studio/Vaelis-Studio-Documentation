# Rigidbody2D

> Vaelis 1.0.0 Rigidbody2D component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/rigidbody2d.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the Rigidbody2D component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector (right) → Add Component → Rigidbody 2D. Pair with Collider 2D for a colliding body. Edit → Physics Layers… controls named layer slots.

## What it does

2D physics body backed by the engine physics runtime. Dynamic, Kinematic and Static bodies have different script controls.

> **Component setup & editor tools:** Rigidbody2D gives an entity a Rapier 2D body. Collider2D is normally paired with it when physical contact is required.

## How to add and use Rigidbody2D

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **Rigidbody2D** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Rigidbody 2D. After adding it, the Rigidbody2D section exposes body type, gravity/damping, velocity/drive values, rotation locking, and controller/ground state fields.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `bodyType` | enum | Dynamic | Kinematic | Static. | `Dynamic` |
| `simulated` | boolean | Whether the body participates in physics simulation. | `true` |
| `mass` | number | Dynamic body mass. | `1` |
| `gravityScale` | number | Gravity multiplier. | `1` |
| `linearDamping` | number | Linear damping. | `0` |
| `angularDamping` | number | Angular damping. | `0.05` |
| `lockRotation` | boolean | Prevent rotation. | `false` |
| `velocityX` | number | X velocity. | `0` |
| `velocityY` | number | Y velocity. | `0` |
| `angularVelocity` | number | Angular velocity. | `0` |
| `driveVelocityX` | number | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `driveVelocityY` | number | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `driveAngularVelocity` | number | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `grounded` | boolean | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `false` |
| `resolvedVelocityX` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `resolvedVelocityY` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingForceX` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingForceY` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingImpulseX` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingImpulseY` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingTorque` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `pendingAngularImpulse` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `mass` | Higher mass makes the body harder to accelerate from the same force/impulse. It does not make gravity itself stronger. |
| `gravityScale` | 1 is the normal engine gravity response for Dynamic bodies; 2 doubles it; 0 disables gravity contribution. |
| `linearDamping` | Higher values remove linear velocity faster; 0 leaves the body with no linear damping. |
| `angularDamping` | Higher values remove rotational velocity faster. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `type` | Property | Dynamic | Kinematic | Static; switching type is supported at runtime. |
| `velocity` | Property | {x,y} velocity. |
| `velocityX` | Property | Horizontal velocity. |
| `velocityY` | Property | Vertical velocity. |
| `mass` | Property | Dynamic mass. |
| `gravityScale` | Property | Gravity multiplier. |
| `linearDamping` | Property | Linear damping. |
| `angularDamping` | Property | Angular damping. |
| `addForce(x,y)` | Method | Apply force to a Dynamic body. |
| `addImpulse(x,y)` | Method | Apply impulse to a Dynamic body. |
| `addTorque(t)` | Method | Apply torque. |
| `addAngularImpulse(t)` | Method | Apply angular impulse. |
| `isGrounded` | Property | Current ground contact state. |
| `move(dx,dy)` | Method | Kinematic movement request. |
| `isOnCeiling` | Property | Kinematic contact state. |
| `isOnWall` | Property | Kinematic contact state. |
| `isOnSlope` | Property | Kinematic contact state. |
| `groundAngle` | Property | Kinematic ground angle. |
| `resolvedVelocity` | Property | Kinematic velocity after collision resolution. |
| `groundAngleLimit` | Property | Maximum angle from horizontal (degrees) that counts as walkable ground for THIS body. |
| `grounded` | Property (read-only) | Deprecated alias for isGrounded — kept for compatibility with existing scripts. |
| `slopeMinAngle` | Property | Minimum groundAngle (degrees) before isOnSlope becomes true. |
| `wallAngleLimit` | Property | Contacts between groundAngleLimit and this angle (degrees) are "too steep" but NOT walls. |

## Notes & behavior

- Kinematic-only methods are meaningful for Kinematic bodies; Dynamic-only force methods apply to Dynamic bodies.
- Position assignment through this.x/this.y is treated as a physics teleport target for non-static bodies.

## Examples

```
this.rigidbody.addImpulse(0, -350);
```

```
this.rigidbody.velocityX = 200;
```

```
this.rigidbody.move(100 * time.deltaTime, 0);
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
