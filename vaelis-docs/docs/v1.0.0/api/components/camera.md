# Camera

> Vaelis 1.0.0 Camera component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/camera.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the Camera component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Camera. Main camera and scaling/presentation settings are edited in the Inspector; Play/Export use the same runtime camera path.

## What it does

Orthographic 2D camera with reference resolutions, responsive scaling, follow, shake and optional pseudo-3D sprite depth scaling.

> **Component setup & editor tools:** Camera controls the 2D view and rendering/scaling behavior. The Scene viewport exposes a camera gizmo when a Camera entity is selected.

## How to add and use Camera

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **Camera** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select the Camera entity → Inspector → Camera. The Camera gizmo appears in the Scene viewport. Mark the intended camera as Main and configure projection/scaling/aspect settings in the Inspector.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `backgroundColor` | hex string | Background color. | `#314D79` |
| `projection` | string | Projection mode. | `Orthographic` |
| `size` | number | Orthographic camera size. | `5` |
| `nearClip` | number | Near clip. | `0.3` |
| `farClip` | number | Far clip. | `1000` |
| `isMain` | boolean | Whether this is the main camera. | `false` |
| `aspectMode` | enum | Landscape | Portrait | Square | Custom. | `Landscape` |
| `landscapeWidth` | number | Landscape reference width. | `960` |
| `landscapeHeight` | number | Landscape reference height. | `540` |
| `portraitWidth` | number | Portrait reference width. | `540` |
| `portraitHeight` | number | Portrait reference height. | `960` |
| `squareSize` | number | Square reference size. | `720` |
| `customWidth` | number | Custom width. | `800` |
| `customHeight` | number | Custom height. | `600` |
| `enablePseudo3D` | boolean | Use Transform.z for sprite depth scaling. | `false` |
| `renderToSpriteEntityId` | string | null | See the Inspector field of the same name. | `null` |
| `scalingMode` | enum | Expand | Fit | Fill | Stretch. | `Fit` |
| `keepHeight` | boolean | Axis choice used by Expand mode. | `true` |
| `aspectRatioLock` | boolean | Lock aspect ratio. | `true` |
| `allowStretching` | boolean | Allow distortion where applicable. | `false` |
| `letterboxing` | enum | Auto | On | Off. | `Auto` |
| `pillarboxing` | enum | Auto | On | Off. | `Auto` |
| `barColor` | hex string | Letterbox/pillarbox color. | `#000000` |
| `integerScaling` | boolean | Use integer scaling. | `false` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `size / zoom` | For this 2D camera, larger effective view size shows more world; increasing zoom makes the scene appear smaller/farther, while reducing it magnifies the world. |
| `scalingMode` | FIT preserves the reference aspect and uses bars when necessary; FILL crops to fill; STRETCH changes aspect; EXPAND keeps the reference height and reveals more/less horizontal world. |
| `integerScaling` | When enabled, device-fit scale is constrained toward integer multiples to keep pixel-art rendering crisp. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `zoom` | Property | Camera zoom/scale control. |
| `backgroundColor` | Property | Background color. |
| `shake(intensity,duration)` | Method | Camera shake. |
| `follow(target, options)` | Method | Follow an entity; options can include smoothing. |
| `stopFollow()` | Method | Stop following. |
| `offsetX` | Property | Follow/render X offset. |
| `offsetY` | Property | Follow/render Y offset. |
| `renderToSprite(spriteEntity)` | Method | Render camera output to a sprite target. |
| `aspectMode` | Property | Landscape | Portrait | Square | Custom. |
| `landscapeWidth` | Property | Landscape reference width. |
| `landscapeHeight` | Property | Landscape reference height. |
| `portraitWidth` | Property | Portrait reference width. |
| `portraitHeight` | Property | Portrait reference height. |
| `squareSize` | Property | Square reference size. |
| `customWidth` | Property | Custom width. |
| `customHeight` | Property | Custom height. |
| `enablePseudo3D` | Property | Enable Transform.z-based sprite depth scaling. |
| `scalingMode` | Property | Expand | Fit | Fill | Stretch. |
| `keepHeight` | Property | Expand axis behavior. |
| `aspectRatioLock` | Property | Aspect lock. |
| `allowStretching` | Property | Allow stretching. |
| `letterboxing` | Property | Auto | On | Off. |
| `pillarboxing` | Property | Auto | On | Off. |
| `barColor` | Property | Bar color. |
| `integerScaling` | Property | Integer scaling. |
| `x` | Property | Camera world-space X position (same as this.x on the camera entity). |
| `y` | Property | Camera world-space Y position (same as this.y on the camera entity). |

## Examples

```
var cam = findFirst("Main Camera");
```

```
cam.camera.follow(findFirst("Target"), { smoothing: 0.1 });
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
