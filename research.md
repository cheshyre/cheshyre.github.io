---
layout: default
title: Research
permalink: /research/
---
{%- comment -%}
The summary is research_summary from the CV's profile.json, in the first person;
scripts/update_pubs.py writes it to _data/derived.json. The highlights come from
_data/highlights.json, in file order (newest first); entries with "hidden": true are left out.
Each is rendered by _includes/highlight.html, which looks up its papers in _data/publications.json.
See README.md for the fields. Without highlights, the page shows only the summary.
{%- endcomment -%}
{%- assign highlights = site.data.highlights | where_exp: "h", "h.hidden != true" -%}

# {% if highlights.size > 0 %}Research highlights{% else %}Research{% endif %}

<p>{{ site.data.derived.research_summary | escape }}</p>

{% if highlights.size > 0 -%}
<div class="highlights">
{%- for item in highlights %}
{% include highlight.html highlight=item %}
{%- endfor %}
</div>
{%- endif %}
