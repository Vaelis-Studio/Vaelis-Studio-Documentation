# Runtime modules

> Vaelis 1.0.0 global scripting and runtime module reference.

- Source: docs/v1.0.0/api/runtime.html
- Engine version: Vaelis 1.0.0

> **Need to know what must exist first?:** Use the API requirements & complete usage map to see prerequisites for every global and component API.

## Global runtime API

| Module/function | Summary |
| --- | --- |
| `findFirst(name)` | Find the first entity by name. |
| `findAll(name)` | Find all entities by name. |
| `findById(id)` | Find one exact entity by stable ID. |
| `findWithTag(tag)` | Find all entities with a tag. |
| `findInRadius(x,y,radius,opts)` | Find nearby entities, nearest first. |
| `scene` | Scene lookup, loading, restart, pause/resume and lighting. |
| `physics` | Raycasts and collision-layer masks. |
| `nav` | Pathfinding, walkability and navigation area utilities. |
| `input` | Keyboard held/pressed state. |
| `mouse` | Cursor position, button state and shape-accurate hit tests. |
| `touch` | Multitouch state plus swipe/pinch gestures. |
| `time` | Frame delta and elapsed game time. |
| `random` | Random integers/floats. |
| `mathx` | Gameplay math helpers. |
| `global` | Transient cross-script state. |
| `save` | Persistent per-slot IndexedDB state. |
| `debug` | On-screen debugging HUD/logging. |
| `spawn()` | Clone authored entities at runtime. |
| `wait()/repeat()` | Entity-owned timers. |
| `sendMessage()` | Targeted or tag-group messaging. |
| `broadcastMessage()` | Scene-wide message broadcast. |

## Fixed update

`onFixedUpdate(dt)` is driven at a fixed 60 Hz accumulator. Keep physics-step decisions here when deterministic cadence matters; use `onUpdate(dt)` for per-render-frame behavior.

## Coordinate spaces

Entity positions, mouse world coordinates, touch world coordinates and raycast points share the game world’s 2D coordinate space. Screen coordinates (`screenX/screenY`) are raw canvas pixels. Camera reference resolutions are separate from world units.
