# NavAgent2D

> Vaelis 1.0.0 NavAgent2D component reference: fields, script API, behavior and examples.

- Source: docs/v1.0.0/api/components/navagent2d.html
- Engine version: Vaelis 1.0.0

> **Scope:** This page documents the NavAgent2D component in Vaelis 1.0.0. Runtime fields are serialized scene data; the Script API section lists only members intentionally exposed to game scripts.

> **Where to find it in the editor:** Inspector → Add Component → Nav Agent 2D. For radius and area painting, use the Nav toolbar after a Nav World 2D exists; Match Collider is in the Nav Agent inspector section.

## What it does

Per-agent navigation settings and current path state for NavWorld2D pathfinding.

> **Component setup & editor tools:** NavAgent2D is the moving-agent side of Vaelis navigation. It works with NavWorld2D and the navigation API.

## How to add and use NavAgent2D

**Editor path:** Select the target entity in the **Hierarchy** (left side) → look at the **Inspector** (right side) → click **Add Component** at the bottom of the Inspector → search for **NavAgent2D** → click the component row. The Add Component picker is a centered modal with a search box; it only lists components not already attached.

For components with a dedicated editor tool, the tool is opened or activated from the location described below. Do not assume that adding the component alone activates its editor; some systems require a separate window, panel, or viewport tool.

## Component setup & editor tools

- Select the agent → Inspector → Add Component → Nav Agent 2D. Configure agent parameters, then use the NavWorld2D + navigation workflow before expecting paths. Runtime movement is driven by the NavAgent2D API.

### What you should see after adding it

The component appears as its own section in the Inspector. Its serialized settings are listed in the **Component data** table below. If a field is conditional, it appears only when the relevant mode/type is selected. If a field is a runtime state field (for example grounded or resolved velocity), treat it as read-only diagnostic state unless the API reference explicitly documents it as writable.

### How to read the settings

For every setting below, the documentation distinguishes **type**, **default**, **meaning**, and tuning direction where behavior is known. When a value represents a direction, use the engine's coordinate convention documented in [Coordinate system](../../reference/coordinate-system.html); do not substitute Unity/Godot conventions.

## Component data

| Field | Type | Purpose | 1.0.0 default |
| --- | --- | --- | --- |
| `radius` | number | Agent clearance radius. | `16` |
| `speed` | number | Preferred speed. | `120` |
| `acceleration` | number | Acceleration. | `800` |
| `deceleration` | number | Deceleration. | `1000` |
| `stoppingDistance` | number | Arrival distance. | `1` |
| `autoRepath` | boolean | Automatically recompute path. | `true` |
| `repathInterval` | number | Minimum seconds between automatic repaths. | `0.35` |
| `repathDistance` | number | Distance target can move before repathing. | `4` |
| `avoidanceEnabled` | boolean | Obstacle/agent avoidance. | `true` |
| `avoidancePriority` | number | Avoidance priority. | `50` |
| `collabEnabled` | boolean | Vehicle/collaborative avoidance mode. | `false` |
| `collabGroupRadius` | number | Collaborative group radius. | `96` |
| `vehicleLookahead` | number | Vehicle path lookahead. | `72` |
| `vehicleCornerLookahead` | number | Corner lookahead. | `110` |
| `vehicleObstacleLookahead` | number | Obstacle lookahead. | `120` |
| `vehicleObstacleWidth` | number | Obstacle width estimate. | `28` |
| `vehicleSteerSmoothing` | number | Steering smoothing. | `7` |
| `vehicleSpeedSmoothing` | number | Speed smoothing. | `5` |
| `vehicleCornerSlowdown` | number | Corner slowdown multiplier. | `0.72` |
| `vehicleObstacleBrake` | number | Obstacle braking factor. | `0.9` |
| `vehicleRecoveryTime` | number | Recovery time. | `1.35` |
| `vehicleRecoveryReverseTime` | number | Reverse recovery time. | `0.9` |
| `area` | 16-bit mask | Allowed navigation areas. | `0xffff` |
| `areaCosts` | array|null | Optional 16-entry per-agent cost overrides. | `null` |
| `currentPath` | value | null | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `null` |
| `currentPathIndex` | number | Written by the engine each frame; not an authored setting. *(engine-managed runtime state)* | `0` |

## Tuning behavior

These are the practical direction-of-change rules for the most important controls on this component.

| Setting | What changing it does |
| --- | --- |
| `radius` | The clearance needed around this agent. Larger radius makes narrow passages become non-walkable for this agent. |
| `speed` | Top travel speed in world units/second. |
| `acceleration / deceleration` | Higher values make movement and stopping snappier; lower values make it softer. |
| `stoppingDistance` | Larger values let the agent stop farther from the final target. |
| `repathInterval` | Lower reacts faster to changing routes/targets but costs more path queries. |
| `area` | Hard allowed-area mask; excluding an area prevents the route from crossing it. |

## Script API

| Member | Kind | Description |
| --- | --- | --- |
| `radius` | Property | Agent radius. |
| `speed` | Property | Preferred speed. |
| `acceleration` | Property | Acceleration. |
| `deceleration` | Property | Deceleration. |
| `stoppingDistance` | Property | Stopping distance. |
| `autoRepath` | Property | Auto-repath. |
| `repathInterval` | Property | Repath interval. |
| `repathDistance` | Property | Target-move repath threshold. |
| `avoidanceEnabled` | Property | Avoidance toggle. |
| `avoidancePriority` | Property | Avoidance priority. |
| `collabEnabled` | Property | Collaborative vehicle avoidance. |
| `collabGroupRadius` | Property | Group radius. |
| `vehicleLookahead` | Property | Vehicle lookahead. |
| `vehicleCornerLookahead` | Property | Corner lookahead. |
| `vehicleObstacleLookahead` | Property | Obstacle lookahead. |
| `vehicleObstacleWidth` | Property | Obstacle width. |
| `vehicleSteerSmoothing` | Property | Steering smoothing. |
| `vehicleSpeedSmoothing` | Property | Speed smoothing. |
| `vehicleCornerSlowdown` | Property | Corner slowdown. |
| `vehicleObstacleBrake` | Property | Obstacle brake factor. |
| `vehicleRecoveryTime` | Property | Recovery time. |
| `vehicleRecoveryReverseTime` | Property | Reverse recovery time. |
| `area` | Property | Allowed area mask. |
| `areaCosts` | Property | 16-entry area cost overrides. |
| `currentPath` | Property | Read-only world-space waypoint array or null. |
| `currentPathIndex` | Property | Read-only current waypoint index. |

## Examples

```
this.navAgent.speed = 180;
```

```
this.navAgent.autoRepath = true;
```

> **Need the full workflow?:** Components: complete workflow covers adding, configuring, testing, combining, and removing components.
