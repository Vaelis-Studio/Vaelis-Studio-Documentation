# this (EntityContext) reference

> Every this.* sub-object reachable inside a script, its required component, and its exact members.

- Source: docs/v1.0.0/api/this.html
- Engine version: Vaelis 1.0.0

> **Need to know what must exist first?:** Use the API requirements & complete usage map to see prerequisites for every global and component API.

## Scope

This page lists every sub-object reachable from `this` inside a script, and what each requires. For the flat shortcuts (`this.x`, `this.position`, etc.) and the lookup/lifecycle helpers (`this.destroy()`, `this.hasComponent()`, `this.isClone`), see Entity shortcuts — this page covers only the per-component sub-objects.

> **Typed errors, not undefined:** Every sub-object below throws a clear, typed error (see Errors & debugging) if accessed on an entity missing the required component, and throws a distinct error on an unknown member name (a typo) rather than returning undefined.

## this.transform

Requires: nothing (every entity has one). Mirrors the flat shortcuts as an object: `position {x,y}`, `rotation`, `scale {x,y}`, `translate(dx, dy)`, `lookAt(x, y)` (rotates to face a point).

## this.rigidbody

Requires: Rigidbody2D. The exposed shape depends on the body’s current `bodyType` (Dynamic / Kinematic / Static) — checked live on every access, so changing `bodyType` at runtime is reflected immediately.

| Member | Dynamic | Kinematic | Static |
| --- | --- | --- | --- |
| velocity, velocityX, velocityY | ✓ | ✓ (drives movement) | — |
| mass, gravityScale, linearDamping, angularDamping | ✓ | — | — |
| addForce(x,y), addImpulse(x,y), addTorque(t), addAngularImpulse(t) | ✓ | — | — |
| move(dx, dy) | — | ✓ | — |
| isGrounded, isOnCeiling, isOnWall, isOnSlope, groundAngle | ✓ | ✓ | — |

```
// Dynamic body — apply forces:
function onUpdate() {
  if (input.keyPressed("Space") && this.rigidbody.isGrounded) {
    this.rigidbody.addImpulse(0, -400);
  }
}

// Kinematic body — drive movement directly:
function onUpdate() {
  this.rigidbody.move(50 * time.deltaTime, 0);
}
```

See Rigidbody2D for what each field means physically.

## this.controller

Requires: CharacterController. Shape depends on `controllerType`. Shared across the walk-family types (Character/Platformer/Top-Down): `moveSpeed`, `acceleration`, `airControl`, `canJump`, `jumpForce`, `maxJumps`, `simulateMove(x,y)`, `simulateJump()`, `isGrounded`/`isOnCeiling`/`isOnWall`/`isOnSlope`/`groundAngle`. Car adds `maxSpeed`, `brakeForce`, `turnSpeed`, `driftFactor`, `simulateDrive(throttle, steer)`, `simulateDriveJoystick(x,y)`, `simulateDriveToward(x,y)`. Follow adds `targetName`, `followSpeed`, `followDistance`. Patrol adds `patrolMode`, `patrolAxis`, `patrolDistance`, `flipDirection()`, `facingDirection`.

## this.collider

Requires: Collider2D. Read-mostly: `shape`, `width`, `height`, `radius`, `offset {x,y}`, `isTrigger`, `isOneWayPlatform`, `friction`, `restitution`, `density`, `layer`, `mask`, and the read-only `isColliding` contact state.

## this.sprite / this.shape / this.text

Requires SpriteRenderer, ShapeRenderer or TextRenderer respectively. See each component’s own reference page for the exact field list — the object shape mirrors the component data one-to-one.

## this.strokePath, this.speechBubble, this.chat, this.textInput, this.joystick

Each requires its matching component (StrokePath, SpeechBubble, ChatLog, TextInput, Joystick) and mirrors that component’s script API — see the component’s own reference page.

## this.animator, this.camera, this.audio, this.ear, this.joint, this.navAgent, this.light, this.shadowCaster

Each requires SpriteAnimation, Camera, AudioSource, AudioListener, Joint2D, NavAgent2D, Light or ShadowCaster respectively, and exposes that component’s documented script API.
