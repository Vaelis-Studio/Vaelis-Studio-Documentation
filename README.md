# Vaelis Studio Documentation

Static documentation site for Vaelis 1.0.0. `index.html` sits at the repository root, so GitHub Pages opens the home page automatically.

## Publish on GitHub Pages
1. Push this folder to a GitHub repository.
2. Settings -> Pages -> Source: "Deploy from a branch", Branch: `main`, folder `/ (root)`.
3. Open `https://<user>.github.io/<repo>/`.

## Layout
- `index.html`: home page (landing)
- `docs/v1.0.0/`: current documentation (`docs/latest/` redirects to it)
- `generator/`: Python build scripts and page sources. Rebuild with `cd generator && python3 build.py --out ..` (add `--origin https://<user>.github.io/<repo>` to fill the sitemap)
- `.nojekyll`: tells GitHub Pages to serve files as they are

## Updating after engine changes
```
cd generator
python3 tools/extract_source_facts.py <engine_root> source-facts.json
node tools/extract_easings.mjs <engine_root> easings.json
python3 build.py --out ..
```
