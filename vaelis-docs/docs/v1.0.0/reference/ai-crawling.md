# AI & crawlers

> How this documentation is structured so search engines and language models can discover and understand Vaelis.

- Source: docs/v1.0.0/reference/ai-crawling.html
- Engine version: Vaelis 1.0.0

> **Recommended retrieval order:** For a UI question, read editor/controls.html first, then the feature page, then the relevant component page. For a script question, read the component/API page plus api/options.json . For a disputed behavior, consult reference/source-map.html and the cited runtime subsystem.

## The important design choice

Core documentation is rendered as ordinary HTML pages with real headings, links, tables and code—not a client-only documentation app. JavaScript enhances navigation/search but does not hold the only copy of the API content.

## Stable version URLs

Every 1.0.0 topic lives under `/docs/v1.0.0/`. Future versions can coexist at their own paths. The root documentation page is a version chooser, while `/docs/latest/` currently aliases the current version.

## Crawler files

| File | Purpose |
| --- | --- |
| `robots.txt` | Allows general crawling and explicitly keeps OpenAI search/training crawlers unblocked unless you change the policy. |
| `sitemap.xml` | Enumerates the HTML and machine-readable URLs for discovery. |
| `llms.txt` | Compact Markdown-style index of the most useful documentation entry points. |
| `llms-full.txt` | Broader index of guide/API/reference pages. |
| `api/v1.0.0/index.json` | Machine-readable engine/component/API catalog. |
| `search-index.json` | Client-side site search index, also easy for tooling to ingest. |

## Publishing correctly

Set `VAELIS_DOCS_ORIGIN` to your real public documentation origin before deployment if you want absolute canonical URLs, sitemap URLs and structured data. Until it is published publicly and not blocked by your crawl rules, no AI service can be expected to discover it.

## OpenAI crawler controls

OpenAI documents separate crawler controls for search and model-training use. The site therefore leaves both `OAI-SearchBot` and `GPTBot` crawlable in `robots.txt`; you can change those directives later if your publishing policy changes.

## AI-friendly API language

API pages state exact member names, types, defaults, return shapes and prerequisites. That is deliberately more useful for code-generating models than prose-only descriptions or a single giant page.
