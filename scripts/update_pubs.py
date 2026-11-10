#!/usr/bin/env python3
"""Regenerate the site's publication and talk data.

Run from the repository root:

    python3 scripts/update_pubs.py              # publications from the INSPIRE-HEP API
    python3 scripts/update_pubs.py --cv DIR     # everything from the CV data folder DIR
    python3 scripts/update_pubs.py --dry-run    # report what would change, write nothing

INSPIRE mode rewrites _data/publications.json from the author's INSPIRE records.

CV mode (--cv DIR) reads the JSON data of the CV (repository cheshyre/resume):
    DIR/publications_inspire.json  ->  _data/publications.json  (converted)
    DIR/talks.json                 ->  _data/talks.json         (converted)
    DIR/<name>.json                ->  _data/<name>.json        (copied unchanged, for the
                                       names in COPIED_FILES below)

Kept from the current _data/publications.json, entry by entry (matched by INSPIRE record id,
then DOI, then arXiv id):
    selected  shown on the home page (in CV mode the CV's own flags are used instead)
    hidden    true to leave the entry off the site
    note      one line under the entry; HTML allowed, e.g., a press-release link
    keep      list of field names this script must not change, e.g., ["title", "authors"]
    title     INSPIRE mode only, because INSPIRE often has the arXiv title in Title Case;
              the script reports titles that differ by more than capitalization
Fields the source leaves empty keep their current value, so a journal added by hand for a
paper in press stays until the source has it. Entries the source does not have (added by
hand) are kept and reported. From the current _data/talks.json, "slides" and "hidden" are
kept for talks with the same date and title.

Standard library only; Python 3.8 or later.
"""

import argparse
import html
import json
import re
import shutil
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBS_FILE = ROOT / "_data" / "publications.json"
TALKS_FILE = ROOT / "_data" / "talks.json"

INSPIRE_API = "https://inspirehep.net/api/literature"
INSPIRE_AUTHOR = "Matthias.Heinz.1"  # INSPIRE author identifier (BAI) of the profile
INSPIRE_RECID = 1817590              # https://inspirehep.net/authors/1817590
OWN_NAME = "M. Heinz"                # must equal author.short_name in _config.yml (shown in bold)

CV_PUBS = "publications_inspire.json"
CV_TALKS = "talks.json"
COPIED_FILES = ["appointments", "awards", "computing", "education", "funding",
                "lectures", "students"]

# Full journal names, keyed by INSPIRE's abbreviation (matched ignoring case, spaces, and dots).
JOURNALS = {
    "Comput.Phys.Commun.": "Computer Physics Communications",
    "Eur.Phys.J.A": "The European Physical Journal A",
    "Few Body Syst.": "Few-Body Systems",
    "J.Phys.G": "Journal of Physics G: Nuclear and Particle Physics",
    "Nature": "Nature",
    "Nature Commun.": "Nature Communications",
    "Nature Phys.": "Nature Physics",
    "Nucl.Phys.A": "Nuclear Physics A",
    "Phys.Lett.B": "Physics Letters B",
    "Phys.Rept.": "Physics Reports",
    "Phys.Rev.A": "Physical Review A",
    "Phys.Rev.C": "Physical Review C",
    "Phys.Rev.D": "Physical Review D",
    "Phys.Rev.Lett.": "Physical Review Letters",
    "Phys.Rev.Res.": "Physical Review Research",
    "Phys.Rev.X": "Physical Review X",
    "Prog.Part.Nucl.Phys.": "Progress in Particle and Nuclear Physics",
    "PRX Quantum": "PRX Quantum",
    "Rev.Mod.Phys.": "Reviews of Modern Physics",
}

# Full institution names for theses, keyed by INSPIRE's name.
INSTITUTIONS = {
    "Darmstadt, Tech. U.": "Technische Universität Darmstadt",
    "Ohio State U.": "The Ohio State University",
}

INVITED_TALK_TYPES = {"invited", "invited_parallel", "plenary", "seminar", "colloquium"}

PUB_KEYS = ["title", "authors", "journal", "volume", "pages", "year", "doi", "arxiv", "type",
            "school", "selected", "note", "hidden", "keep", "inspire"]
TALK_KEYS = ["title", "event", "city", "date", "invited", "type", "virtual", "award", "slides",
             "hidden"]
FILLABLE = ["journal", "volume", "pages", "doi", "arxiv", "school"]


# --- LaTeX to Unicode and HTML -------------------------------------------------------------

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
           "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030c", "H": "\u030b",
           "c": "\u0327", "k": "\u0328", "r": "\u030a", "b": "\u0331", "d": "\u0323"}
LETTERS = {"ss": "ß", "ae": "æ", "AE": "Æ", "oe": "œ", "OE": "Œ", "aa": "å", "AA": "Å",
           "o": "ø", "O": "Ø", "l": "ł", "L": "Ł", "i": "i", "j": "j"}
ESCAPES = {"&": "&", "%": "%", "_": "_", "#": "#", "$": "$", "{": "{", "}": "}"}
GREEK = {name: chr(code) for name, code in [
    ("alpha", 0x3B1), ("beta", 0x3B2), ("gamma", 0x3B3), ("delta", 0x3B4), ("epsilon", 0x3B5),
    ("varepsilon", 0x3B5), ("zeta", 0x3B6), ("eta", 0x3B7), ("theta", 0x3B8), ("iota", 0x3B9),
    ("kappa", 0x3BA), ("lambda", 0x3BB), ("mu", 0x3BC), ("nu", 0x3BD), ("xi", 0x3BE),
    ("pi", 0x3C0), ("rho", 0x3C1), ("sigma", 0x3C3), ("tau", 0x3C4), ("upsilon", 0x3C5),
    ("phi", 0x3C6), ("varphi", 0x3C6), ("chi", 0x3C7), ("psi", 0x3C8), ("omega", 0x3C9),
    ("Gamma", 0x393), ("Delta", 0x394), ("Theta", 0x398), ("Lambda", 0x39B), ("Xi", 0x39E),
    ("Pi", 0x3A0), ("Sigma", 0x3A3), ("Phi", 0x3A6), ("Psi", 0x3A8), ("Omega", 0x3A9)]}
SYMBOLS = {"to": "→", "rightarrow": "→", "leftarrow": "←", "leftrightarrow": "↔",
           "times": "×", "pm": "±", "mp": "∓", "cdot": "·", "sim": "∼", "approx": "≈",
           "simeq": "≃", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠",
           "infty": "∞", "ell": "ℓ", "hbar": "ℏ", "prime": "′", "langle": "⟨", "rangle": "⟩",
           "partial": "∂", "nabla": "∇", "dagger": "†", "star": "⋆", "circ": "∘",
           "textrightarrow": "→", "ldots": "…", "dots": "…"}
UPRIGHT = {"mathrm", "text", "textrm", "rm", "operatorname", "mathrm*"}
SPACES = {",": "\u2009", ";": " ", ":": " ", " ": " ", "!": "", "quad": " ", "qquad": " "}


def latex_to_unicode(s):
    """Convert LaTeX accents and special letters in plain text (names, titles) to Unicode."""
    s = re.sub(r"\\textbf\s*\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(ss|ae|AE|oe|OE|aa|AA|o|O|l|L|i|j)(?![A-Za-z])\s*",
               lambda m: LETTERS[m.group(1)], s)

    def accent(m):
        return m.group(2) + ACCENTS[m.group(1)]

    s = re.sub(r"\\(['`^\"~=.])\s*\{?\s*([A-Za-z])\s*\}?", accent, s)
    s = re.sub(r"\\([uvHckrbd])\s*\{\s*([A-Za-z])\s*\}", accent, s)
    s = re.sub(r"\\([uvHckrbd])\s+([A-Za-z])", accent, s)
    s = re.sub(r"\\([&%_#$])", lambda m: ESCAPES[m.group(1)], s)
    s = s.replace("---", "—").replace("--", "–").replace("~", " ")
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\s+", " ", s)
    return unicodedata.normalize("NFC", s)


class _Math:
    """Tiny converter for the inline formulas that appear in titles, e.g., $^{48}$Ca or $N=32$."""

    def __init__(self, src):
        self.s, self.i = src, 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def group(self, upright):
        """One argument: a braced group or a single token."""
        while self.peek() == " ":
            self.i += 1
        if self.peek() == "{":
            self.i += 1
            out = self.run(upright, stop="}")
            self.i += 1
            return out
        if self.peek() == "\\":
            return self.command(upright)
        ch = self.peek()
        self.i += 1
        return self.char(ch, upright)

    def command(self, upright):
        self.i += 1
        m = re.match(r"[A-Za-z]+\*?|.", self.s[self.i:])
        name = m.group(0) if m else ""
        self.i += len(name)
        if name in UPRIGHT:
            return self.group(True)
        if name in GREEK:
            return GREEK[name]
        if name in SYMBOLS:
            return SYMBOLS[name]
        if name in SPACES:
            return SPACES[name]
        if name in ESCAPES:
            return html.escape(ESCAPES[name], quote=False)
        if name in ("mathit", "textit", "mathbf", "textbf", "ensuremath", "boldsymbol"):
            return self.group(upright)
        return html.escape(name, quote=False)

    def char(self, ch, upright):
        if ch.isalpha() and not upright:
            return "<i>" + ch + "</i>"
        if ch == "=":
            return " = "
        if ch == "-":
            return "−"
        if ch == "'":
            return "′"
        return html.escape(ch, quote=False)

    def run(self, upright=False, stop=""):
        out = []
        while self.i < len(self.s) and self.peek() != stop:
            ch = self.peek()
            if ch == "\\":
                out.append(self.command(upright))
            elif ch == "^":
                self.i += 1
                out.append("<sup>" + self.group(upright) + "</sup>")
            elif ch == "_":
                self.i += 1
                out.append("<sub>" + self.group(upright) + "</sub>")
            elif ch == "{":
                self.i += 1
                out.append(self.run(upright, stop="}"))
                self.i += 1
            else:
                self.i += 1
                out.append(self.char(ch, upright))
        text = "".join(out).replace("</i><i>", "")
        return re.sub(r" {2,}", " ", text)


def title_to_html(title):
    """Title with $...$ formulas -> text with <sup>, <sub>, and <i> where needed."""
    parts = re.split(r"(?<!\\)\$", title or "")
    out = []
    for k, part in enumerate(parts):
        if k % 2:
            out.append(_Math(part).run().strip())
        else:
            out.append(html.escape(latex_to_unicode(part), quote=False) if part.strip() else part)
    text = "".join(out)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def plain(text):
    """Comparison key: title without tags, case, punctuation, or spacing."""
    text = re.sub(r"<[^>]+>", "", html.unescape(text or ""))
    return re.sub(r"[\W_]+", "", text.casefold())


def name_from_latex(raw):
    """CV export author ('Z.~Y.~Xu', '\\textbf{M.~Heinz}') -> display name."""
    if "\\textbf" in raw:
        return OWN_NAME
    return latex_to_unicode(raw).strip()


def _abbreviate(token):
    if "-" in token:
        return "-".join(_abbreviate(p) for p in token.split("-") if p)
    if token.endswith("."):
        parts = [p for p in token.split(".") if p]
        return " ".join(p + "." for p in parts) if len(parts) > 1 else token
    return token[0] + "."


def name_from_inspire(author):
    """INSPIRE author ({'full_name': 'Heinz, Matthias', ...}) -> 'M. Heinz'."""
    ref = (author.get("record") or {}).get("$ref", "")
    if ref.rstrip("/").endswith("/authors/%d" % INSPIRE_RECID):
        return OWN_NAME
    full = (author.get("full_name") or "").strip()
    if "," not in full:
        return full
    last, rest = full.split(",", 1)
    first, _, suffix = rest.partition(",")
    initials = " ".join(_abbreviate(t) for t in first.split())
    name = (initials + " " + last.strip()).strip()
    return name + (", " + suffix.strip() if suffix.strip() else "")


def _key(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


_JOURNAL_KEYS = {_key(k): v for k, v in JOURNALS.items()}
_journal_cache = {}


def journal_name(abbrev, ref=None):
    """INSPIRE journal abbreviation -> full name (table above, else the INSPIRE journal record)."""
    if not abbrev:
        return None
    if _key(abbrev) in _JOURNAL_KEYS:
        return _JOURNAL_KEYS[_key(abbrev)]
    if ref and ref not in _journal_cache:
        try:
            meta = fetch_json(ref)["metadata"]
            _journal_cache[ref] = (meta.get("journal_title") or {}).get("title")
        except Exception:  # network or format problem: fall back to the abbreviation
            _journal_cache[ref] = None
    full = _journal_cache.get(ref) or abbrev
    print("note: journal %r is not in JOURNALS; using %r" % (abbrev, full))
    return full


# --- Sources -------------------------------------------------------------------------------

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": "update_pubs.py (matthiasheinz.com)"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def records_from_inspire():
    fields = ["control_number", "titles", "authors.full_name", "authors.record", "dois",
              "arxiv_eprints", "document_type", "publication_info", "imprints",
              "preprint_date", "earliest_date", "thesis_info"]
    query = {"q": "a " + INSPIRE_AUTHOR, "size": "250", "sort": "mostrecent",
             "fields": ",".join(fields)}
    url = INSPIRE_API + "?" + urllib.parse.urlencode(query)
    records = []
    while url:
        data = fetch_json(url)
        records += [record_from_inspire(hit["metadata"]) for hit in data["hits"]["hits"]]
        url = (data.get("links") or {}).get("next")
        if url:
            time.sleep(1)
    return records


def record_from_inspire(md):
    skip = {"erratum", "addendum", "reprint", "translation", "editorial note"}
    pubinfo = [p for p in md.get("publication_info", [])
               if p.get("journal_title") and p.get("material") not in skip]
    pi = pubinfo[0] if pubinfo else {}
    doc = md.get("document_type") or []
    if "thesis" in doc:
        kind = "thesis"
    elif "conference paper" in doc or "proceedings" in doc:
        kind = "proceedings"
    else:
        kind = "article"
    pages = pi.get("artid") or pi.get("page_start")
    if pages and not pi.get("artid") and pi.get("page_end"):
        pages = "%s–%s" % (pi["page_start"], pi["page_end"])
    thesis = md.get("thesis_info") or {}
    imprint = (md.get("imprints") or [{}])[0].get("date")
    date = (imprint if pi else None) or md.get("preprint_date") or imprint \
        or thesis.get("date") or md.get("earliest_date") or ""
    year = pi.get("year") or (int(date[:4]) if date[:4].isdigit() else None)
    school = None
    if kind == "thesis":
        names = [i.get("name") for i in thesis.get("institutions", []) if i.get("name")]
        school = INSTITUTIONS.get(names[0], names[0]) if names else None
    return {
        "recid": md.get("control_number"),
        "title": ((md.get("titles") or [{}])[0]).get("title", ""),
        "authors": [name_from_inspire(a) for a in md.get("authors", [])],
        "journal": journal_name(pi.get("journal_title"), (pi.get("journal_record") or {}).get("$ref")),
        "volume": pi.get("journal_volume"),
        "pages": pages,
        "year": year,
        "doi": ((md.get("dois") or [{}])[0]).get("value"),
        "arxiv": ((md.get("arxiv_eprints") or [{}])[0]).get("value"),
        "type": kind,
        "school": school,
        "date": date,
        "selected": None,
    }


def record_from_cv(p):
    t = (p.get("type") or "").lower()
    if t in ("phdthesis", "mastersthesis", "thesis"):
        kind = "thesis"
    elif t in ("inproceedings", "proceedings", "conference"):
        kind = "proceedings"
    else:
        kind = "article"
    school = p.get("school")
    return {
        "recid": p.get("recid"),
        "title": p.get("title_text") or p.get("title") or "",
        "authors": [name_from_latex(a) for a in p.get("authors", [])],
        "journal": p.get("journal"),
        "volume": p.get("volume"),
        "pages": p.get("pages"),
        "year": p.get("year"),
        "doi": p.get("doi"),
        "arxiv": p.get("arxiv"),
        "type": kind,
        "school": INSTITUTIONS.get(school, school) if school else None,
        "date": p.get("date") or "",
        "selected": bool(p["selected"]) if "selected" in p else None,
    }


# --- Publications --------------------------------------------------------------------------

def entry_from_record(r):
    e = {"title": title_to_html(r["title"]), "authors": r["authors"]}
    for k in ("journal", "volume", "pages"):
        if r.get(k):
            e[k] = str(r[k])
    if r.get("year"):
        e["year"] = int(r["year"])
    for k in ("doi", "arxiv"):
        if r.get(k):
            e[k] = r[k]
    e["type"] = r["type"]
    if r["type"] == "thesis" and r.get("school"):
        e["school"] = r["school"]
    e["selected"] = r.get("selected")  # None: the source has no flags; keep the file's
    e["inspire"] = r["recid"]
    e["_date"] = r.get("date") or ""
    return e


def find_old(e, old):
    for key in ("inspire", "doi", "arxiv"):
        for o in old:
            if e.get(key) and o.get(key) == e.get(key):
                return o
    return None


def merge_pubs(new, old, cv_mode):
    report, used = [], set()
    for e in new:
        o = find_old(e, old)
        if o is None:
            e["selected"] = bool(e["selected"])
            if old:
                report.append("new: %s (%s)" % (plain_title(e), e.get("year")))
            continue
        used.add(id(o))
        for k in ("hidden", "note", "keep"):
            if k in o:
                e[k] = o[k]
        if e["selected"] is None:
            e["selected"] = bool(o.get("selected"))
        if not cv_mode:
            if o.get("title"):
                if plain(o["title"]) != plain(e["title"]) and "title" not in o.get("keep", []):
                    report.append("title differs on INSPIRE, kept yours: %s | INSPIRE: %s"
                                  % (plain_title(o), plain_title(e)))
                e["title"] = o["title"]
        for k in FILLABLE:
            if not e.get(k) and o.get(k):
                e[k] = o[k]
        for k in o.get("keep", []):
            if k in o:
                e[k] = o[k]
        changed = [k for k in PUB_KEYS if k != "inspire" and o.get(k) != e.get(k)]
        if changed:
            report.append("changed %s: %s" % (", ".join(changed), plain_title(e)))
    manual = [dict(o, _date="") for o in old if id(o) not in used]
    for o in manual:
        report.append("kept (not in the source): %s" % plain_title(o))
    entries = new + manual
    # Newest year first; within a year, preprints and papers in press first; then by date.
    entries.sort(key=lambda e: e.get("_date", ""), reverse=True)
    entries.sort(key=lambda e: e.get("type") == "thesis" or bool(e.get("volume") or e.get("pages")))
    entries.sort(key=lambda e: e.get("year") or 0, reverse=True)
    return [ordered(e, PUB_KEYS) for e in entries], report


def plain_title(e):
    return re.sub(r"<[^>]+>", "", html.unescape(e.get("title", "")))[:80]


# --- Talks ---------------------------------------------------------------------------------

def talks_from_cv(cv_talks, old):
    def match_key(t):
        return (t.get("date"), plain(t.get("title")), plain(t.get("event")))

    old_by_key = {}
    for t in old:
        old_by_key.setdefault(match_key(t), []).append(t)
    out, report = [], []
    for t in cv_talks:
        e = {"title": title_to_html(t.get("title", "")), "event": t.get("event"),
             "city": t.get("location"), "date": t.get("date"),
             "invited": t.get("type") in INVITED_TALK_TYPES}
        if t.get("type"):
            e["type"] = t["type"]
        if t.get("virtual"):
            e["virtual"] = True
        if t.get("award"):
            e["award"] = t["award"]
        matches = old_by_key.get(match_key(e))
        o = matches.pop(0) if matches else None
        if o is None and old:
            report.append("new talk: %s (%s)" % (plain_title(e), e["date"]))
        for k in ("slides", "hidden"):
            if o and k in o:
                e[k] = o[k]
        out.append(ordered(e, TALK_KEYS))
    for rest in old_by_key.values():
        for o in rest:
            report.append("dropped (not in the CV): %s (%s)" % (plain_title(o), o.get("date")))
    return out, report


# --- Files ---------------------------------------------------------------------------------

def ordered(e, keys):
    out = {k: e[k] for k in keys if k in e and e[k] is not None}
    out.update({k: v for k, v in e.items() if k not in out and not k.startswith("_")
                and v is not None})
    if "inspire" in out:  # keep the record id last
        out["inspire"] = out.pop("inspire")
    return out


def dumps(entries):
    """One key per line; lists such as authors stay on one line."""
    lines = ["["]
    for i, e in enumerate(entries):
        lines.append("  {")
        items = list(e.items())
        for j, (k, v) in enumerate(items):
            comma = "," if j < len(items) - 1 else ""
            lines.append("    %s: %s%s" % (json.dumps(k), json.dumps(v, ensure_ascii=False), comma))
        lines.append("  }" + ("," if i < len(entries) - 1 else ""))
    lines.append("]")
    return "\n".join(lines) + "\n"


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save(path, entries, dry_run):
    text = dumps(entries)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        print("%s: unchanged (%d entries)" % (path.relative_to(ROOT), len(entries)))
    elif dry_run:
        print("%s: would write %d entries" % (path.relative_to(ROOT), len(entries)))
    else:
        path.write_text(text, encoding="utf-8")
        print("%s: wrote %d entries" % (path.relative_to(ROOT), len(entries)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cv", metavar="DIR", type=Path,
                    help="read the CV data folder instead of the INSPIRE API")
    ap.add_argument("--dry-run", action="store_true", help="report changes, write nothing")
    args = ap.parse_args(argv)

    if args.cv:
        cv = json.loads((args.cv / CV_PUBS).read_text(encoding="utf-8"))
        cv = cv["publications"] if isinstance(cv, dict) else cv
        records = [record_from_cv(p) for p in cv]
    else:
        records = records_from_inspire()
    if not records:
        sys.exit("no publications found; nothing written")
    pubs, report = merge_pubs([entry_from_record(r) for r in records], load(PUBS_FILE),
                              cv_mode=bool(args.cv))
    for line in report:
        print("  " + line)
    save(PUBS_FILE, pubs, args.dry_run)

    if args.cv:
        talks_path = args.cv / CV_TALKS
        if talks_path.exists():
            cv_talks = json.loads(talks_path.read_text(encoding="utf-8"))
            talks, report = talks_from_cv(cv_talks, load(TALKS_FILE))
            for line in report:
                print("  " + line)
            save(TALKS_FILE, talks, args.dry_run)
        for name in COPIED_FILES:
            src, dst = args.cv / (name + ".json"), ROOT / "_data" / (name + ".json")
            if not src.exists():
                continue
            json.loads(src.read_text(encoding="utf-8"))  # stop here if it is not valid JSON
            if dst.exists() and dst.read_bytes() == src.read_bytes():
                continue
            print("%s: %s" % (dst.relative_to(ROOT), "would copy" if args.dry_run else "copied"))
            if not args.dry_run:
                shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
