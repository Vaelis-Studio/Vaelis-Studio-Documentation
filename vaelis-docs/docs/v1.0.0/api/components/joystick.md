# Joystick

> Vaelis 1.0.0 Joystick component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/joystick.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the Joystick component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Top UI → Joystick, or Inspector → Add Component → Joystick.

## What it does

Virtual touch joystick for mobile and pointer-driven control schemes.

> **Component setup & editor tools:** Joystick provides a touch/drag virtual control for mobile-oriented input.

## How to add and use Joystick

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **Joystick** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- GameObject → UI → Joystick creates a joystick entity. You can also select an entity → Inspector → Add Component → Joystick.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `positionMode` | enum | Fixed or pointer-positioned joystick. | `Fixed` |
| `regionX` | number | Region X. | `0` |
| `regionY` | number | Region Y. | `0` |
| `regionWidth` | number | Region width. | `640` |
| `regionHeight` | number | Region height. | `720` |
| `baseRadius` | number | Base radius. | `60` |
| `knobRadius` | number | Knob radius. | `28` |
| `baseColor` | hex string | Base color. | `#ffffff` |
| `baseOpacity` | number | Base opacity. | `0.25` |
| `knobColor` | hex string | Knob color. | `#ffffff` |
| `knobOpacity` | number | Knob opacity. | `0.6` |
| `outlineColor` | hex string | Outline color. | `#ffffff` |
| `outlineWidth` | number | Outline width. | `2` |
| `deadZone` | number | Input dead zone. | `0.1` |
| `returnToCenter` | boolean | Knob returns to center when released. | `true` |
| `hideWhenIdle` | boolean | Hide when idle. | `false` |
| `idleOpacityMultiplier` | number | Opacity multiplier while idle. | `0.35` |
| `x` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `y` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `magnitude` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `angle` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `active` | boolean | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `false` |
| `baseScreenX` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |
| `baseScreenY` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `deadZone` | 0 means even tiny stick displacement is reported; increasing it keeps small movements at zero until the knob moves farther. |
| `baseRadius / knobRadius` | Larger values make the on-screen joystick physically larger. |
| `idleOpacityMultiplier` | Lower makes an idle joystick more transparent when hideWhenIdle is false. |
| `returnToCenter` | True snaps back on release; false preserves the last knob position. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `x` | Property | Normalized horizontal input, typically -1..1 (read-only). |
| `y` | Property | Normalized vertical input, typically -1..1 (read-only). |
| `magnitude` | Property | Input magnitude (read-only). |
| `angle` | Property | Input angle (read-only). |
| `active` | Property | Whether the joystick is engaged (read-only). |
| `positionMode` | Property | Joystick positioning mode. |
| `regionX` | Property | Touch/pointer region X. |
| `regionY` | Property | Touch/pointer region Y. |
| `regionWidth` | Property | Region width. |
| `regionHeight` | Property | Region height. |
| `baseRadius` | Property | Base radius. |
| `knobRadius` | Property | Knob radius. |
| `deadZone` | Property | Dead-zone threshold. |
| `returnToCenter` | Property | Return-to-center behavior. |
| `baseColor` | Property | Available on this module. |
| `baseOpacity` | Property | Available on this module. |
| `hideWhenIdle` | Property | true = invisible until actively being dragged. |
| `idleOpacityMultiplier` | Property | Available on this module. |
| `knobColor` | Property | Available on this module. |
| `knobOpacity` | Property | Available on this module. |
| `outlineColor` | Property | Available on this module. |
| `outlineWidth` | Property | Available on this module. |

## Examples

```
this.rigidbody.velocityX = this.joystick.x * 250;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
