# CharacterController

> Vaelis 1.0.0 CharacterController component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/charactercontroller.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the CharacterController component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Movement Type. Pick Character Controller, Platformer, Top-Down, Car, Follow or Patrol; fields in the Inspector change with the selected mode.

## What it does

High-level movement modes: Character Controller, Platformer, Top-Down, Car, Follow, Patrol and Free.

> **Component setup & editor tools:** CharacterController provides the higher-level movement behaviors such as Platformer, Car, Follow, or Patrol when configured with the required physics components.

## How to add and use CharacterController

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **CharacterController** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select entity → Inspector → Add Component → Movement Type (CharacterController). Choose the controller type first; the Inspector then exposes the relevant movement fields. Platformer/Car/Follow/Patrol fields are not interchangeable—configure only the group belonging to the selected controller type.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `controllerType` | enum | Character Controller | Platformer | Top-Down | Car | Follow | Patrol | Free. | `Character Controller` |
| `moveSpeed` | number | General movement speed. | `200` |
| `acceleration` | number | Acceleration. | `20` |
| `airControl` | number | Air control multiplier. | `0.5` |
| `canJump` | boolean | Jump enabled. | `true` |
| `jumpForce` | number | Jump impulse/velocity. | `420` |
| `maxJumps` | integer | Maximum sequential jumps. | `1` |
| `useGravity` | boolean | Use gravity where supported. | `true` |
| `gravityScale` | number | Gravity multiplier. | `1` |
| `useDefaultInput` | boolean | Use built-in input mapping. | `true` |
| `maxSpeed` | number | Car maximum speed. | `350` |
| `carAcceleration` | number | Car acceleration. | `200` |
| `brakeForce` | number | Car braking force. | `400` |
| `turnSpeed` | number | Car turning speed. | `150` |
| `driftFactor` | number | Car drift behavior. | `0.92` |
| `driveTowardArriveDistance` | number | Car drive-toward arrival distance. | `12` |
| `targetName` | string | Follow target entity name. |  |
| `followSpeed` | number | Follow speed. | `150` |
| `followDistance` | number | Follow spacing. | `5` |
| `patrolDistance` | number | Patrol distance. | `150` |
| `patrolMode` | enum | Platformer | Top-Down. | `Platformer` |
| `patrolAxis` | enum | Horizontal | Vertical. | `Horizontal` |
| `requestJump` | boolean | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `false` |
| `requestMoveX` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestMoveY` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestThrottle` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestSteer` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestJoystickX` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestJoystickY` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestDriveTowardX` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestDriveTowardY` | value | null | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `null` |
| `requestFlip` | boolean | Set transiently by the engine (controller/navigation input); not an authored setting. *(engine-managed runtime state)* | `false` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `moveSpeed` | Higher = faster target movement. |
| `acceleration` | Higher = reaches the requested speed faster; lower = softer/slower ramp. |
| `airControl` | For Platformer, 0 removes horizontal air steering; 1 gives full ground-like acceleration in air. |
| `jumpForce` | Higher = stronger/faster upward launch; lower = shorter jump. |
| `gravityScale` | 1 = normal controller gravity, 0 = no controller gravity; higher magnifies the pull. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `controllerType` | Property | Read-only movement type. |
| `moveSpeed` | Property | Movement speed. |
| `acceleration` | Property | Acceleration. |
| `airControl` | Property | Air-control factor. |
| `useGravity` | Property | Gravity toggle. |
| `gravityScale` | Property | Gravity scale. |
| `useDefaultInput` | Property | Built-in input mapping. |
| `simulateMove(x,y)` | Method | Drive movement by script. |
| `isGrounded` | Property | Ground state. |
| `isOnCeiling` | Property | Ceiling contact. |
| `isOnWall` | Property | Wall contact. |
| `isOnSlope` | Property | Slope contact. |
| `groundAngle` | Property | Ground angle. |
| `canJump` | Property | Whether jumping is available. |
| `jumpForce` | Property | Jump force. |
| `maxJumps` | Property | Maximum jumps. |
| `simulateJump()` | Method | Request a jump. |
| `maxSpeed` | Property | Car maximum speed. |
| `brakeForce` | Property | Car brake force. |
| `turnSpeed` | Property | Car turn speed. |
| `driftFactor` | Property | Car drift factor. |
| `simulateDrive(throttle, steer)` | Method | Drive a Car controller by script. |
| `simulateDriveJoystick(x,y)` | Method | Drive using joystick-style vector input. |
| `simulateDriveToward(x,y)` | Method | Drive toward a world point. |
| `targetName` | Property | Follow target name. |
| `followSpeed` | Property | Follow speed. |
| `followDistance` | Property | Follow distance. |
| `patrolMode` | Property | Platformer | Top-Down. |
| `patrolAxis` | Property | Horizontal | Vertical. |
| `patrolDistance` | Property | Patrol distance. |
| `flipDirection()` | Method | Reverse Patrol direction. |
| `facingDirection` | Property | Current patrol facing direction. |
| `driveTowardArriveDistance` | Property | Available on this module. |

## Notes & behavior

- Car-only fields/actions are meaningful for the Car controller. Patrol has its own patrolMode and patrolAxis. Free is script-driven with no built-in input mapping.

## Examples

```
this.controller.simulateMove(input.keyDown("ArrowRight") ? 1 : 0, 0);
```

```
this.controller.simulateJump();
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
