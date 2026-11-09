# matthiasheinz.com

Source of my research website. GitHub Pages builds it with Jekyll from the `main` branch and serves it at <https://cheshyre.github.io> (and at <https://matthiasheinz.com> once the custom domain is connected).

Design C, "Quiet modern": one layout (`_layouts/default.html`), one stylesheet (`assets/css/site.css`), no JavaScript. Placeholder text is marked `[like this]`.

## Files

| Path | What it holds |
| --- | --- |
| `_config.yml` | Title, description, position line, photo path, and profile links (email, INSPIRE, ORCID, GitHub) |
| `_data/nav.yml` | Top bar navigation |
| `_data/publications.json` | Publications; entries with `"selected": true` also appear on the home page |
| `_data/talks.json` | Talks |
| `_includes/pub.html` | How one publication row is rendered |
| `index.md`, `research.md`, `publications.md`, `cv.md`, `teaching.md` | The five pages |
| `assets/cv.pdf` | The CV download (add it) |
| `assets/img/` | The portrait photo (add it, then set `photo:` in `_config.yml`) |

## Preview locally

Needs Ruby 3 and Bundler.

```sh
bundle install                 # once; installs the github-pages gem, the same Jekyll GitHub uses
bundle exec jekyll serve       # then open http://localhost:4000
```

The page reloads on refresh after edits; restart the server after changing `_config.yml`. A warning that GitHub Metadata found no API authentication is harmless.

## Add a paper

Add an object to `_data/publications.json` (valid JSON: commas between entries, none after the last):

```json
{
  "title": "In-medium similarity renormalization group with three-body operators",
  "authors": ["M. Heinz", "A. Tichai", "J. Hoppe", "K. Hebeler", "A. Schwenk"],
  "journal": "Phys. Rev. C",
  "volume": "103",
  "page": "044318",
  "year": 2021,
  "doi": "10.1103/PhysRevC.103.044318",
  "arxiv": "2102.11172",
  "selected": true
}
```

`doi` and `arxiv` are the bare identifiers; the links are built from them. Every article gets both where available. Optional: `note` (e.g., "Letter" or "submitted"). Lists are sorted by `year`, newest first.

## Add a talk

Add an object to `_data/talks.json`:

```json
{
  "title": "Talk title",
  "event": "Workshop or conference name",
  "location": "City, Country",
  "date": "2026-11-09",
  "type": "Invited talk",
  "url": "",
  "slides": ""
}
```

Use absolute dates (`YYYY-MM-DD`). `url`, `slides`, and `type` are optional.

## Update the CV

1. Replace `assets/cv.pdf` with the new PDF (keep the file name so the link stays the same).
2. Update the HTML summary in `cv.md` if positions, education, or honors changed.
3. Commit and push to `main`; GitHub Pages rebuilds within a minute or two.

## Writing conventions

American spelling, the Oxford comma, and ", e.g., " and ", i.e., " set off with commas. Dates are absolute.

## Limits

Only plugins supported by the `github-pages` gem (currently `jekyll-seo-tag` and `jekyll-sitemap`). No secrets, tokens, or private details in this repository: it is public.
