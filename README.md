# matthiasheinz.com

Source of my research website. GitHub Pages builds it with Jekyll from the `main` branch and serves it at <https://cheshyre.github.io> (and at <https://matthiasheinz.com> once the custom domain is connected).

Design C, "Quiet modern": one layout (`_layouts/default.html`), one stylesheet (`assets/css/site.css`), no JavaScript. Placeholder text is marked `[like this]`.

## Files

| Path | What it holds |
| --- | --- |
| `_config.yml` | Title and description for search results, photo path, and GitHub link (everything else about you comes from the CV data) |
| `_data/nav.yml` | Top bar navigation |
| `_data/publications.json` | Publications; entries with `"selected": true` also appear on the home page |
| `_data/talks.json` | Talks and posters |
| `_data/appointments.json`, `awards.json`, `computing.json`, `education.json`, `funding.json`, `lectures.json`, `profile.json`, `students.json` | Copies of the CV data (repository `cheshyre/resume`), used by every page |
| `_data/derived.json` | Research summary in the first person and its first two sentences, written by the script from `profile.json` |
| `_data/highlights.json` | Research highlights on the research page (written here, not part of the CV data) |
| `_data/funders.json` | Funding logos on the home page (not part of the CV data) |
| `_includes/pub.html`, `_includes/talk.html` | How one publication or talk row is rendered |
| `_includes/highlight.html` | How one research highlight is rendered |
| `_includes/when.html`, `_includes/thousands.html` | Small helpers: years of a CV item, and numbers with thousands separators |
| `index.md`, `research.md`, `publications.md`, `cv.md`, `teaching.md` | The five pages |
| `assets/cv.pdf` | The CV download (copied by the script from `cv_public.pdf`) |
| `assets/img/` | The portrait photo, funding logos (`funding/`), and highlight figures (`research/`) |
| `scripts/update_pubs.py` | Regenerates the data files from INSPIRE or from the CV data (not published) |

## Preview locally

Needs Ruby 3 and Bundler.

```sh
bundle install                 # once; installs the github-pages gem, the same Jekyll GitHub uses
bundle exec jekyll serve       # then open http://localhost:4000
```

The page reloads on refresh after edits; restart the server after changing `_config.yml`. A warning that GitHub Metadata found no API authentication is harmless.

## Update publications, talks, and CV data

Everything on the site that describes you comes from the CV data, except the photo, the GitHub link, the research interests, the research highlights, the funding logos, and the page and section texts. `scripts/update_pubs.py` needs only Python 3.8 or later. Run it from the repository root, check the diff, and commit.

```sh
python3 scripts/update_pubs.py --cv ../resume/data # everything from the CV data folder
python3 scripts/update_pubs.py                     # only publications, from INSPIRE
python3 scripts/update_pubs.py --dry-run           # report what would change, write nothing
```

- **CV mode** (`--cv DIR`) converts `publications_inspire.json` and `talks.json`, copies the other JSON files and `cv_public.pdf` (as `assets/cv.pdf`), and writes `_data/derived.json` from `profile.json`. Point it at the folder that holds the CV's JSON files.
- **INSPIRE mode** rewrites `_data/publications.json` from the INSPIRE profile linked in `_data/profile.json`. Titles already in the file are kept, because INSPIRE often has the arXiv title in Title Case; the script reports titles that differ by more than capitalization.
- **Both modes** then report papers cited in `_data/highlights.json` that have no entry, or a hidden one, in the new `_data/publications.json`.

The site shows the CV data as is. CV mode rebuilds `_data/publications.json` and `_data/talks.json` from the export alone, so do not edit them by hand: change the CV data instead (details that only the CV PDF has stay in the PDF). The script lists what changed. INSPIRE mode keeps the `selected` flags, `hidden` flags, and titles already in the file.

Do not copy the CV's `talks.json` or `publications_inspire.json` into `_data/` directly: the site uses different field names, which the script converts.

### What the site reads from each CV file

| CV file | Used for |
| --- | --- |
| `profile.json` | Name, position line, email, INSPIRE, ORCID, Google Scholar, your name in author lists (`author_name`), the research summary (research page) and its first two sentences (home page) |
| `appointments.json` | Appointments on the home and CV pages |
| `awards.json` | CV awards; those with `"highlight": true` are the home page's honors (`hidden` entries are left out everywhere) |
| `funding.json`, `computing.json` | CV funding and computing grants (the home page shows the logos in `_data/funders.json` instead) |
| `education.json` | Education on the home and CV pages |
| `lectures.json`, `students.json` | Teaching page |
| `publications_inspire.json` | Publications page and the home page's selected publications |
| `talks.json` | Talks on the publications page |
| `cv_public.pdf` | The CV download |

### Optional fields the script and pages already understand

None of these are in the CV data yet:

- `profile.json`: `research_summary_first_person` (used as is instead of the automatic conversion of `research_summary`), `interests` (a list of `{"title": ..., "text": ...}`, shown as the home page's research interests instead of the four written in `index.md`), and `links.github`.
- `publications_inspire.json`, per entry: `hidden` (`true` leaves the entry off the site).
- `talks.json`, per talk: `slides` (URL, shown as a link) and `hidden`.

## Publication entries

```json
{
  "title": "In-medium similarity renormalization group with three-body operators",
  "authors": ["M. Heinz", "A. Tichai", "J. Hoppe", "K. Hebeler", "A. Schwenk"],
  "journal": "Physical Review C",
  "volume": "103",
  "pages": "044318",
  "year": 2021,
  "doi": "10.1103/PhysRevC.103.044318",
  "arxiv": "2102.11172",
  "type": "article",
  "selected": true,
  "inspire": 1847789
}
```

- `title` may contain `<sup>`, `<sub>`, and `<i>` for formulas (e.g., `<sup>48</sup>Ca`); the script writes them from INSPIRE's LaTeX.
- `authors`: your own name, written exactly as `author_name` in `_data/profile.json` (`M. Heinz`), is set in bold. Lists of more than 10 authors show the first five, your name, and "et al."
- `journal`, `volume`, `pages`: entries without a journal are shown as "Preprint".
- `doi` and `arxiv` are the bare identifiers; the links are built from them. Every article gets both where available.
- `type`: `article`, `proceedings`, or `thesis`. Theses get their own section and may have `school`.
- `selected`: `true` for the entries on the home page (in file order).
- Optional: `hidden` (`true` to leave the entry off the site).
- `inspire` is the INSPIRE record id; the script uses it to match entries. Leave it out for papers that are not on INSPIRE.

The file is sorted newest year first, preprints first within a year; the pages show entries in file order.

## Talk entries

```json
{
  "title": "NuLattice: Computations of nuclei on lattices",
  "event": "CRC 1245 Workshop",
  "city": "Mainz, Germany",
  "date": "2026-09",
  "invited": true,
  "type": "invited"
}
```

`date` is `YYYY-MM` and shown as month and year. `invited` is `true` for invited talks, plenary talks, seminars, and colloquia. Optional: `type` (`invited`, `invited_parallel`, `plenary`, `seminar`, `colloquium`, `contributed`, or `poster`; sets the label, e.g., "Invited talk" or "Poster"), `virtual`, `award`, `slides`, and `hidden`. Without a `type`, invited talks are labeled "Invited". Talks are listed newest first, in file order.

## Research highlights

The research page shows the entries of `_data/highlights.json` after the research summary, in file order (newest first). Each has a heading, a figure on the right (above the text on phones), one paragraph, and the papers it is based on. Without entries, the page shows only the summary under the title "Research", and the home page leaves out its "Research highlights →" link.

```json
{
  "title": "Heading of the highlight",
  "text": "One paragraph on the result and why it matters.",
  "papers": [2851666],
  "figure": "/assets/img/research/calcium.png",
  "alt": "What the figure shows, for readers who cannot see it"
}
```

- `title` and `text` are written by hand and may contain `<sup>`, `<sub>`, and `<i>` (e.g., `<sup>48</sup>Ca`).
- `papers`: the papers the highlight is based on, as identifiers of entries in `_data/publications.json`: the INSPIRE record id (preferred), the DOI, or the arXiv id. Each is shown as a publication row looked up from that file, so titles, authors, journals, and the DOI and arXiv links are never retyped. An identifier without an entry is shown as a bracketed note, and `scripts/update_pubs.py` reports it.
- `figure` and `alt`: an image under `assets/img/research/` that you may publish, and its alt text. SVG works best; otherwise PNG or JPEG at least 1000 px wide (shown up to 320 px wide on desktops and at full width on phones). Without a figure, the text takes the full width.
- Optional: `hidden` (`true` leaves the entry off the site).

## Funding logos

The home page's Funding section shows the logos in `_data/funders.json`, in file order, each linked to the funder's page. List current funding only; the CV page lists all funding and computing grants from the CV data.

```json
{
  "name": "RIKEN TRIP",
  "full_name": "Transformative Research Innovation Platform of RIKEN platforms",
  "logo": "/assets/img/funding/riken-trip.svg",
  "url": "https://trip.riken.jp/en/"
}
```

`name` and the optional `full_name` form the alt text; `url` is optional. Logos are shown 112 px high (96 px on phones), so crop them to the drawing; SVG works best. `riken-trip.svg` was converted from the vector PDF of the logo with `pdftocairo -svg`, cropped to the drawing, and compacted.

## Update the CV

1. Run `python3 scripts/update_pubs.py --cv DIR`; it copies the new `cv_public.pdf` to `assets/cv.pdf` and refreshes every page's data.
2. Commit and push to `main`; GitHub Pages rebuilds within a minute or two.

## Writing conventions

American spelling, the Oxford comma, and ", e.g., " and ", i.e., " set off with commas. Dates are absolute.

## Limits

Only plugins supported by the `github-pages` gem (currently `jekyll-seo-tag` and `jekyll-sitemap`). No secrets, tokens, or private details in this repository: it is public.

## License

- Code (layouts, includes, stylesheet, scripts, and configuration): MIT License, see [`LICENSE`](LICENSE).
- Content (page text, publication and talk lists, and the CV): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Photographs and third-party material are excluded.
