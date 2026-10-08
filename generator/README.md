# Vaelis documentation generator

Renders `content/**/*.html` (page bodies) into a fully static, crawlable site: sidebar/TOC/search UI, Markdown twins,
`llms.txt`, `llms-full.txt`, search index, API catalog, sitemap and robots.txt.

```bash
pip install beautifulsoup4 lxml markdownify pygments
python3 tools/extract_source_facts.py /path/to/vaelis-engine source-facts.json   # re-read the engine source
python3 build.py --out ../vaelis-docs --origin https://docs.example.com          # --origin enables sitemap + canonicals
```

* `content/` — one fragment per page; first line is `<!--meta {"title","description","lede"} -->`.
* `lib/patch.py` — rewrites component field tables and script-API tables from `source-facts.json`, so the docs cannot drift from the source.
* `lib/htmlx.py` — callouts, code highlighting, tables, heading anchors. `static/` — CSS/JS. `build.py` — navigation + everything else.
* New engine version: copy `content/` to a new tree, bump `VERSION` in `build.py`, keep the old output folder untouched.
