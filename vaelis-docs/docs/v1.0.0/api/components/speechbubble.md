# SpeechBubble

> Vaelis 1.0.0 SpeechBubble component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/speechbubble.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the SpeechBubble component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Top UI → Speech Bubble, or Inspector → Add Component → Speech Bubble.

## What it does

Speech bubble UI attached to an entity, useful for dialogue and NPC callouts.

> **Component setup & editor tools:** SpeechBubble provides an in-scene speech presentation attached to an entity.

## How to add and use SpeechBubble

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **SpeechBubble** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Inspector → SpeechBubble: configure its display properties; use the documented SpeechBubble API to change content at runtime.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `text` | string | Current bubble text. | `Hello!` |
| `visible` | boolean | Whether visible. | `false` |
| `backgroundColor` | hex string | Bubble background. | `#ffffff` |
| `textColor` | hex string | Text color. | `#111111` |
| `borderColor` | hex string | Border color. | `#111111` |
| `borderWidth` | number | Border width. | `2` |
| `fontSize` | number | Font size. | `20` |
| `fontFamily` | string | Font family. | `Arial` |
| `padding` | number | Bubble padding. | `12` |
| `cornerRadius` | number | Corner radius. | `10` |
| `maxWidth` | number | Maximum text width. | `220` |
| `offsetX` | number | World/UI X offset. | `0` |
| `offsetY` | number | World/UI Y offset. | `-60` |
| `tailDirection` | enum | Tail direction. | `down` |
| `tailSize` | number | Tail size. | `14` |
| `hideTimer` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `maxWidth` | Higher lets a line run longer before wrapping. |
| `offsetY` | Negative values move the bubble upward from the entity in the default screen convention. |
| `padding` | Higher creates more interior space around text. |
| `cornerRadius` | Higher makes corners rounder. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `text` | Property | Current text. |
| `visible` | Property | Visibility. |
| `backgroundColor` | Property | Background color. |
| `textColor` | Property | Text color. |
| `borderColor` | Property | Border color. |
| `borderWidth` | Property | Border width. |
| `fontSize` | Property | Font size. |
| `fontFamily` | Property | Font family. |
| `padding` | Property | Padding. |
| `cornerRadius` | Property | Corner radius. |
| `maxWidth` | Property | Maximum width. |
| `offsetX` | Property | Horizontal offset. |
| `offsetY` | Property | Vertical offset. |
| `tailDirection` | Property | Tail direction. |
| `tailSize` | Property | Tail size. |
| `show(text, duration)` | Method | Set text and show; optional duration hides automatically. |
| `hide()` | Method | Hide the bubble. |

## Examples

```
this.speechBubble.show("Hello!", 2);
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
