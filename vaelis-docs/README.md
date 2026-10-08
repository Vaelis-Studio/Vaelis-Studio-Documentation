# Vaelis documentation — v1.0.0

Static site: upload this folder to any static host (Vercel, Netlify, GitHub Pages, S3…) or preview with
`python3 -m http.server 8000`. Pages also open directly from disk (client-side navigation is simply skipped on `file://`).

* Every page is complete HTML (works with JavaScript off) and has a Markdown twin at the same URL with `.md`.
* For AI/crawlers: `llms.txt`, `llms-full.txt` (all docs in one file), `search-index.json`, `api/v1.0.0/index.json`, `robots.txt`, `sitemap.xml`.
* Before publishing, rebuild with your real origin so `sitemap.xml` and canonical URLs are absolute:
  `python3 ../generator/build.py --origin https://your-domain.example`
* Add a new version by publishing `docs/v1.1.0/` alongside `docs/v1.0.0/`; never overwrite old versions.
