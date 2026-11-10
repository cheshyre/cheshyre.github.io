---
layout: default
title: Publications and talks
permalink: /publications/
---
{%- comment -%}
Articles (grouped by year), then theses, then talks, in the order of _data/publications.json and
_data/talks.json (both newest first; scripts/update_pubs.py keeps them sorted). Entries with
"hidden": true are left out. See README.md for the fields.
{%- endcomment -%}

# Publications and talks

My publications are also listed, with citation counts, on [INSPIRE]({{ site.links.inspire }}) and [Google Scholar]({{ site.links.scholar }}).

{% assign shown = site.data.publications | where_exp: "p", "p.hidden != true" -%}
{%- assign articles = shown | where_exp: "p", "p.type != 'thesis'" -%}
{%- assign theses = shown | where: "type", "thesis" -%}

## Articles

<div class="pubs">
{%- assign last = "" -%}
{%- for p in articles -%}
{%- assign y = p.year | append: "" -%}
{%- if y == last -%}{%- assign hide = true -%}{%- else -%}{%- assign hide = false -%}{%- endif %}
{% include pub.html pub=p hide_year=hide %}
{%- assign last = y -%}
{%- endfor %}
</div>

{% if theses.size > 0 -%}
## {% if theses.size > 1 %}Theses{% else %}Thesis{% endif %}

<div class="pubs">
{%- for p in theses %}
{% include pub.html pub=p %}
{%- endfor %}
</div>
{%- endif %}

## Talks and posters

{% assign talks = site.data.talks | where_exp: "t", "t.hidden != true" -%}
<div class="pubs">
{%- assign last = "" -%}
{%- for t in talks -%}
{%- assign y = t.date | slice: 0, 4 -%}
{%- if y == last -%}{%- assign hide = true -%}{%- else -%}{%- assign hide = false -%}{%- endif %}
{% include talk.html talk=t hide_year=hide %}
{%- assign last = y -%}
{%- endfor %}
</div>
