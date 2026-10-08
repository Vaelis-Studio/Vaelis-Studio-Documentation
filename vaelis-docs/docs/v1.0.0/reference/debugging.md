# Debugging

> Diagnose common Vaelis runtime and authoring problems.

- Source: docs/v1.0.0/reference/debugging.html
- Engine version: Vaelis 1.0.0

## Use the Debug HUD

The `debug` module can show the HUD, FPS and logging. Performance/profiling displays are useful while diagnosing update and rendering behavior.

## Lifecycle failures

If a lifecycle callback throws, the runtime reports the error and isolates it. Look for the callback name and error classification in the runtime output.

## Physics checklist

- Confirm the entity has the expected Rigidbody2D body type.
- Confirm Collider2D shape, layer and mask settings.
- For one-way platforms, test motion from both sides.
- Use `physics.raycast(...,{debug:true})` to verify what the query actually sees.

## Navigation checklist

- Confirm a NavWorld2D exists in the scene.
- Confirm the queried point is inside walkable bounds.
- Check NavAgent2D radius/area settings.
- Use `nav.findPath(...,{debug:true})` to visualize the result.

## Common API mistake

> **Editor code is not game code:** If code is only found in project/editor/ , it is not automatically a supported game-script API. The public script surface is the documented this.\* context and global runtime modules.
