# Versioning

> Vaelis engine version policy and documentation version strategy.

- Source: docs/v1.0.0/reference/versioning.html
- Engine version: Vaelis 1.0.0

## Semantic version rules

| Increment | Use for |
| --- | --- |
| MAJOR | Scene/manifest-format-breaking changes. |
| MINOR | New backward-compatible engine features. |
| PATCH | Fixes that do not change save-format compatibility. |

## Why docs are versioned

API details and serialized scene formats can evolve. Keep `/docs/v1.0.0/` intact when 1.1.0 or 2.0.0 ships, then add a new version directory and version entry. This keeps old tutorials and AI-generated code anchored to the engine version they target.

## Adding a new version

```
docs/v1.0.0/
docs/1.1.0/
docs/2.0.0/

# Then update versions.json and regenerate the site.
```

## Compatibility warning

The engine itself compares incoming project manifest versions against the current editor version and warns when a project comes from a newer engine. Treat the documented version in generated code and scene data as part of the compatibility context.

> **Stable versioned URLs.:** Each engine version has its own URL namespace, such as /docs/v1.0.0/ . When a new engine version is released, publish it under a new path such as /docs/v1.1.0/ instead of replacing the older version. This keeps old projects and AI/search results tied to the documentation version they were built against.
