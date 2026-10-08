# ChatLog

> Vaelis 1.0.0 ChatLog component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/chatlog.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the ChatLog component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Top UI → Chat Log, or Inspector → Add Component → Chat Log.

## What it does

Scrollable-style conversation log component for UI dialogue.

> **Component setup & editor tools:** ChatLog provides a dialogue/log display component intended for scripted text updates.

## How to add and use ChatLog

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **ChatLog** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Inspector → ChatLog: configure the log; use its script-facing API for runtime messages/entries.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `messages` | array | Current messages. | `[]` |
| `maxMessages` | number | Maximum retained messages. | `50` |
| `visibleCount` | number | Messages visible at once. | `6` |
| `width` | number | Log width. | `320` |
| `lineHeight` | number | Line height. | `26` |
| `fontSize` | number | Font size. | `16` |
| `fontFamily` | string | Font family. | `Arial` |
| `messageColor` | hex string | Message color. | `#ffffff` |
| `senderColor` | hex string | Sender name color. | `#ffd700` |
| `backgroundColor` | hex string | Background. | `#000000` |
| `backgroundOpacity` | number | Background opacity. | `0.5` |
| `padding` | number | Padding. | `10` |
| `showSender` | boolean | Show sender names. | `true` |
| `screenSpace` | boolean | Use screen-space UI behavior. | `true` |
| `visible` | boolean | Visibility. | `true` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `maxMessages` | Total retained history before oldest messages are dropped. |
| `visibleCount` | How many recent messages are shown at once. |
| `backgroundOpacity` | 0 transparent, 1 opaque. |
| `lineHeight` | Higher creates more vertical spacing between messages. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `messages` | Property | Read-only snapshot of messages {sender,text,senderColor}. |
| `maxMessages` | Property | Maximum retained messages. |
| `visibleCount` | Property | Number of visible rows. |
| `width` | Property | Panel width. |
| `lineHeight` | Property | Line height. |
| `fontSize` | Property | Font size. |
| `fontFamily` | Property | Font family. |
| `messageColor` | Property | Message color. |
| `senderColor` | Property | Default sender color. |
| `backgroundColor` | Property | Background color. |
| `backgroundOpacity` | Property | Background opacity. |
| `padding` | Property | Padding. |
| `showSender` | Property | Show sender names. |
| `screenSpace` | Property | Screen-space mode. |
| `visible` | Property | Visibility. |
| `send(sender, text, color)` | Method | Append a message. |
| `clear()` | Method | Clear the log. |

## Examples

```
this.chat.send("Guard", "Halt!", "#ef4444");
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
