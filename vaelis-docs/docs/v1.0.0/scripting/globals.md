# Global API

> Reference the global objects and functions available inside Vaelis scripts.

- Source: docs/v1.0.0/scripting/globals.html
- Engine version: Vaelis 1.0.0

## Entity lookup

| API | Purpose |
| --- | --- |
| findFirst(name) | First entity matching a name, or null. |
| findAll(name) | Every entity with a name, as an array. |
| findFirstWithTag(tag) | First entity with a tag, or null. |
| findAllWithTag(tag) | Every entity with a tag. |
| findWithTag(tag) | Alias for findAllWithTag(). |
| findById(id) | Exact entity by stable ID, or null. |
| findInRadius(x,y,radius,opts) | Entities within radius, nearest first; optional name/tag filter. |

```
function onUpdate() {
  var target = findFirst("Target");
  if (target) this.navMoveToward(target.x, target.y, 100);

  var nearby = findInRadius(this.x, this.y, 150, { tag: "Enemy" });
  debug.log("Enemies nearby", nearby.length);
}
```

## Scene, physics & navigation modules

| Module | Key members |
| --- | --- |
| scene | current, load, restart, pause, resume, isPaused, lighting, find\* |
| physics | raycast, layer |
| nav | findPath, isWalkable, bake, areaIndex, areaMask, areaCosts |

```
function onTriggerEnter(other) {
  if (other.name === "Target") scene.load("Level2");
}

function onUpdate() {
  var hit = physics.raycast(this.x, this.y, this.x + 200, this.y);
  if (hit) debug.log("Ray hit", hit.entity ? hit.entity.name : "wall");
}
```

## Spawning & scheduling

| API | Semantics |
| --- | --- |
| spawn(nameOrTag, options) | Clone authored entity; supports direct entity contexts and byTag lookup. |
| wait(seconds, callback) | One-shot timer; returns a timer ID. |
| repeat(seconds, callback) | Recurring timer; returns a timer ID. |
| cancelWait(timerId) | Cancel one-shot timer. |
| cancelRepeat(timerId) | Cancel recurring timer. |

```
function onStart() {
  spawn("Enemy", { x: this.x + 100, y: this.y });

  this._spawnTimer = repeat(2, function () {
    spawn("Coin", { x: Math.random() * 400, y: 0 });
  });
}

function onDestroy() {
  cancelRepeat(this._spawnTimer);
}
```

## Messaging

`sendMessage(tagOrEntity, message, data)` can address every entity in a tag or one exact entity context. `broadcastMessage(message, data)` sends to all scene entities. Message handlers use the same script context model.

```
// Sender:
function onCollisionEnter(other) {
  sendMessage("Enemy", "hit", { amount: 10 });
}

// Receiver (on any entity tagged "Enemy"):
function onMessage(message, sender, data) {
  if (message === "hit") this.hp -= data.amount;
}
```

## Math & time

Use `time.deltaTime` and `time.elapsed`; `random.int()`/`random.float()`; and the small `mathx` helpers `lerp`, `clamp`, `moveToward`, `remap` and `approximately`. Native JavaScript `Math` is also available.

```
function onUpdate() {
  this.x = mathx.moveToward(this.x, targetX, 200 * time.deltaTime);
  this.rotation = mathx.lerp(this.rotation, 90, 0.1);
  if (random.float() < 0.01) spawn("Powerup", { x: this.x, y: this.y });
}
```
