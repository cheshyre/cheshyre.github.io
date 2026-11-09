---
layout: default
title: Publications and talks
permalink: /publications/
---
{%- comment -%}
Lists every entry in _data/publications.json and _data/talks.json, newest first.
See README.md for the fields of each entry.
{%- endcomment -%}

# Publications and talks

[One sentence pointing to your INSPIRE profile for the complete, up-to-date list.]

## Publications

{% assign pubs = site.data.publications | sort: "year" | reverse -%}
<div class="pubs">
{%- for p in pubs %}
{% include pub.html pub=p %}
{%- else %}
<div class="pub"><span class="pub-year">[year]</span><div><p class="pub-title placeholder">[Publications appear here from _data/publications.json]</p></div></div>
{%- endfor %}
</div>

## Talks

{% assign talks = site.data.talks | sort: "date" | reverse -%}
<div class="pubs">
{%- for t in talks %}
<div class="pub">
<span class="pub-year">{{ t.date | slice: 0, 4 }}</span>
<div>
<p class="pub-title">{% if t.url %}<a href="{{ t.url }}">{{ t.title }}</a>{% else %}{{ t.title }}{% endif %}</p>
<p class="pub-meta">{{ t.event }}{% if t.location %}, {{ t.location }}{% endif %}{% if t.date %} · {{ t.date | date: "%B %-d, %Y" }}{% endif %}{% if t.type %} · {{ t.type }}{% endif %}{% if t.slides %} · <a href="{{ t.slides }}">Slides</a>{% endif %}</p>
</div>
</div>
{%- else %}
<div class="pub"><span class="pub-year">[year]</span><div><p class="pub-title placeholder">[Talks appear here from _data/talks.json]</p></div></div>
{%- endfor %}
</div>
