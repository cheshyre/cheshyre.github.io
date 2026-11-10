# matthiasheinz.com

Source of my research website. GitHub Pages builds it with Jekyll from the `main` branch and serves it at <https://cheshyre.github.io> (and at <https://matthiasheinz.com> once the custom domain is connected).

Design C, "Quiet modern": one layout (`_layouts/default.html`), one stylesheet (`assets/css/site.css`), no JavaScript. Placeholder text is marked `[like this]`.

## Files

| Path | What it holds |
| --- | --- |
| `_config.yml` | Title, description, name as it appears in author lists, position line, photo path, and profile links (email, INSPIRE, ORCID, Google Scholar, GitHub) |
| `_data/nav.yml` | Top bar navigation |
| `_data/publications.json` | Publications; entries with `"selected": true` also appear on the home page |
| `_data/talks.json` | Talks and posters |
| `_data/appointments.json`, `awards.json`, `computing.json`, `education.json`, `funding.json`, `lectures.json`, `students.json` | Copies of the CV data (repository `cheshyre/resume`), used by the home, CV, and teaching pages |
| `_includes/pub.html`, `_includes/talk.html` | How one publication or talk row is rendered |
| `_includes/when.html`, `_includes/thousands.html` | Small helpers: years of a CV item, and numbers with thousands separators |
| `index.md`, `research.md`, `publications.md`, `cv.md`, `teaching.md` | The five pages |
| `assets/cv.pdf` | The CV download |
| `assets/img/` | The portrait photo |
| `scripts/update_pubs.py` | Regenerates the data files from INSPIRE or from the CV data (not published) |

## Preview locally

Needs Ruby 3 and Bundler.

```sh
bundle install                 # once; installs the github-pages gem, the same Jekyll GitHub uses
bundle exec jekyll serve       # then open http://localhost:4000
```

The page reloads on refresh after edits; restart the server after changing `_config.yml`. A warning that GitHub Metadata found no API authentication is harmless.

## Update publications, talks, and CV data

`scripts/update_pubs.py` needs only Python 3.8 or later. Run it from the repository root, check the diff, and commit.

```sh
python3 scripts/update_pubs.py                     # publications from INSPIRE (profile 1817590)
python3 scripts/update_pubs.py --cv ../resume/data # everything from the CV data folder
python3 scripts/update_pubs.py --dry-run           # report what would change, write nothing
```

- **INSPIRE mode** rewrites `_data/publications.json` from the INSPIRE records. Titles already in the file are kept, because INSPIRE often has the arXiv title in Title Case; the script reports titles that differ by more than capitalization.
- **CV mode** (`--cv DIR`) converts `DIR/publications_inspire.json` and `DIR/talks.json`, and copies the other CV files listed above unchanged. The CV's `selected` flags and titles are used. Point it at the folder that holds the CV's JSON files.

Either way, the script keeps what you set by hand in `_data/publications.json`: `selected` (INSPIRE mode), `hidden`, `note`, `keep`, and any field the source leaves empty (e.g., the journal of a paper in press). For talks it keeps `slides` and `hidden`. Entries the source does not have are kept and reported.

Do not copy the CV's `talks.json` or `publications_inspire.json` into `_data/` directly: the site uses different field names, which the script converts.

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
- `authors`: your own name, written exactly as `author.short_name` in `_config.yml` (`M. Heinz`), is set in bold. Lists of more than 10 authors show the first five, your name, and "et al."
- `journal`, `volume`, `pages`: a journal without volume and pages is shown as "(in press)"; no journal shows "Preprint".
- `doi` and `arxiv` are the bare identifiers; the links are built from them. Every article gets both where available.
- `type`: `article`, `proceedings`, or `thesis`. Theses get their own section and may have `school`.
- `selected`: `true` for the entries on the home page (in file order).
- Optional: `note` (one line under the entry, HTML allowed, e.g., a press-release link), `hidden` (`true` to leave the entry off the site), and `keep` (fields the script must not change, e.g., `["title", "authors"]`).
- `inspire` is the INSPIRE record id; the script uses it to match entries. Leave it out for papers that are not on INSPIRE.

The file is sorted newest year first, preprints and papers in press first within a year; the pages show entries in file order.

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

## Update the CV

1. Replace `assets/cv.pdf` with the new PDF (keep the file name so the link stays the same).
2. Run `python3 scripts/update_pubs.py --cv DIR` to refresh the lists on the home, CV, teaching, and publications pages.
3. Commit and push to `main`; GitHub Pages rebuilds within a minute or two.

## Writing conventions

American spelling, the Oxford comma, and ", e.g., " and ", i.e., " set off with commas. Dates are absolute.

## Limits

Only plugins supported by the `github-pages` gem (currently `jekyll-seo-tag` and `jekyll-sitemap`). No secrets, tokens, or private details in this repository: it is public.

## License

- Code (layouts, includes, stylesheet, scripts, and configuration): MIT License, see [`LICENSE`](LICENSE).
- Content (page text, publication and talk lists, and the CV): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Photographs and third-party material are excluded.
