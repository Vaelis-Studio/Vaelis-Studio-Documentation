# Editor settings & performance

> Window menu panels, File menu storage options, Inspector component notes, Console buttons and the performance settings that cap editor and game frame rates.

- Source: docs/v1.0.0/editor/settings.html
- Engine version: Vaelis 1.0.0

## Window menu

The **Window** menu in the top toolbar shows or hides the three big panels. Each row is a checkbox.

| Item | Panel |
| --- | --- |
| Hierarchy | Left column. |
| Asset Panel | Bottom strip (Console and Project tabs). |
| Inspector | Right column. |
| Show All Panels | Appears only while at least one panel is hidden; restores all three. |

Hiding a panel removes its column and the Scene viewport grows into the freed space. The choice is remembered across reloads per browser, not per project. Only an explicit hide is saved, so a damaged value can never leave you without a way to get panels back.

## File menu storage options

| Item | What it does |
| --- | --- |
| Save Now / Saved | Saves immediately instead of waiting for the next auto-save and reports whether it worked. Shows *Saved* when nothing has changed. |
| Save Project | Downloads a re-loadable project file. |
| Optimize Assets on Save: ON / OFF | When ON, Save Project losslessly re-encodes PNGs and repacks WAV audio before zipping. Smaller file, slower save. Off by default. |
| Load Project… | Opens a `.vs` or `.zip` project. If the project contains scripts the editor asks for confirmation first. |
| Export… | Opens the [Export window](../export/export-window.html). |
| Enable Extra Backup Storage… | Pick a folder on your real disk; every auto-save is also mirrored there, beyond the browser's storage limit. The menu then shows *Extra Backup Storage: ON (click to turn off)*; turning it off only stops future mirroring and deletes nothing. |
| Restore from Backup Folder… | Appears while backup is on. Loads the last mirrored version of this project, replacing what is open. |

## Inspector component notes

The small **info (i)** button at the right of the Inspector tab bar shows or hides the grey explanatory notes under each component. Notes are **off by default** so an entity with many components stays compact. The setting is remembered. Orange warnings (for example a missing Collider 2D) are always shown regardless of this toggle.

## Console panel

The Console tab in the bottom panel collects script output and engine messages from Play. Use **Copy** to copy the log text and **Clear** to empty it. Console text is shown as plain text, never interpreted as HTML.

## Performance settings

The engine keeps a small performance settings object in the browser's `localStorage` under the key `vaelis_engine_settings`. Missing or invalid fields fall back to their defaults individually. In 1.0.0 these values are read by the editor and Play window; there is no settings dialog yet, so changing them means editing that stored value.

| Setting | Default | Meaning |
| --- | --- | --- |
| `editorFpsFocused` | 60 | Frame cap for the editor viewport while its window is focused. |
| `editorFpsUnfocused` | 24 | Frame cap while the editor is not focused, to save power. |
| `gameFps` | 60 | Frame cap for the Play window. Allowed values: 30, 60, 120, or 0 for unlimited. |
| `backgroundRendering` | true | Keep the editor rendering (throttled) when unfocused instead of pausing fully. |
| `vsync` | true | Stored toggle for vertical sync. |
| `showComponentNotes` | false | The Inspector notes toggle described above. |

The Play window applies `gameFps` through the game loop's target FPS. **Exported games are not capped**: they run unlimited (0) and use whatever frame rate the device sustains. The bottom **status bar** shows live FPS, memory and object count, and the engine version.

> **Game-side debug HUD:** Inside Play, call debug.show() from a script to see FPS and per-system frame times, and debug.log("label", value) to add your own lines. See Global API .

## Memory protection

While a game runs, a memory watchdog monitors JavaScript heap use. If it climbs past a high threshold the engine runs a safe reclaim pass: it asks the GPU texture collector to evict unused textures, drops regenerable placeholder textures and sweeps stale render caches. Textures and audio used by the live scene are never wiped, so sprites do not turn into missing-texture markers.
