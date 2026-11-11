---
layout: default
title: Home
---
{%- comment -%}
Home page, built from the CV data in _data (see README.md):
  name, position, email, INSPIRE, ORCID, Google Scholar: profile.json
  statement: first two sentences of the research summary (derived.json, from profile.json)
  research interests: "interests" in profile.json if present, else the four below
  selected publications: publications.json entries with "selected": true, in file order
  education, appointments: education.json and appointments.json, in file order
  honors: entries of awards.json with "highlight": true, in file order
  funding: logos of current funders from _data/funders.json, in file order (not in the CV data;
    the CV page lists all funding and computing grants from funding.json and computing.json)
Set in _config.yml: the photo and the GitHub link (not in the CV data).
HTML here is kept flush left so Markdown does not turn indented lines into code blocks.
{%- endcomment -%}
{%- assign profile = site.data.profile -%}
{%- assign name = profile.name | default: site.author.name -%}
<section class="hero">
<div class="hero-text">
<h1>{{ name }}</h1>
<p class="position">{{ profile.position }}, {{ profile.institution }}</p>
<p class="statement">{{ site.data.derived.research_statement | escape }}</p>
<p class="links">
{%- assign email = profile.emails | first -%}
{%- assign github = profile.links.github | default: site.links.github -%}
{%- if email %}<a href="mailto:{{ email }}">Email</a>{% endif -%}
{%- if profile.links.inspire %}<a href="{{ profile.links.inspire }}">INSPIRE</a>{% endif -%}
{%- if profile.orcid %}<a href="https://orcid.org/{{ profile.orcid }}">ORCID</a>{% endif -%}
{%- if profile.links.google_scholar %}<a href="{{ profile.links.google_scholar }}">Google Scholar</a>{% endif -%}
{%- if github and github != "" %}<a href="{{ github }}">GitHub</a>{% endif -%}
</p>
</div>
{%- if site.photo != "" %}
<img class="photo" src="{{ site.photo | relative_url }}" alt="Portrait of {{ name }}" width="176" height="176">
{%- else %}
<div class="photo" role="img" aria-label="Portrait placeholder">[Photo]</div>
{%- endif %}
</section>

<section class="section">
<h2 class="label">Research interests</h2>
<div class="grid-2">
{%- if profile.interests %}
{%- for i in profile.interests %}
<div><p class="item-title">{{ i.title | default: i }}</p>{% if i.text %}<p class="item-text">{{ i.text }}</p>{% endif %}</div>
{%- endfor %}
{%- else %}
<div><p class="item-title">Precision many-body methods</p><p class="item-text">Scalable and systematically improvable ab initio calculations.</p></div>
<div><p class="item-title">Heavy and neutron-rich nuclei</p><p class="item-text">Shell structure, charge radii, neutron skins, and the limits of stability.</p></div>
<div><p class="item-title">Physics beyond the standard model</p><p class="item-text">Nuclear matrix elements for searches for new physics in atoms and nuclei.</p></div>
<div><p class="item-title">Computing for nuclear theory</p><p class="item-text">Advanced computational technologies, including quantum computing and leadership computing.</p></div>
{%- endif %}
</div>
</section>

<section class="section">
<div class="section-head">
<h2 class="label">Selected publications</h2>
<a href="{{ '/publications/' | relative_url }}">All publications and talks →</a>
</div>
{%- assign selected = site.data.publications | where: "selected", true | where_exp: "p", "p.hidden != true" %}
<div class="pubs">
{%- for p in selected %}
{% include pub.html pub=p %}
{%- else %}
<div class="pub"><span class="pub-year">[year]</span><div><p class="pub-title placeholder">[Selected publications appear here: entries in _data/publications.json with "selected": true]</p></div></div>
{%- endfor %}
</div>
</section>

<section class="split">
<div>
<h2 class="label">Education</h2>
<ul class="dated wide">
{%- for e in site.data.education %}
<li><span class="year">{% include when.html item=e %}</span><span>{{ e.degree }}, {{ e.institution }}</span></li>
{%- endfor %}
</ul>
</div>
<div>
<h2 class="label">Appointments</h2>
<ul class="dated wide">
{%- for a in site.data.appointments %}
<li><span class="year">{% include when.html item=a %}</span><span>{{ a.title }}, {{ a.institution }}</span></li>
{%- endfor %}
</ul>
</div>
</section>

<section class="split">
{%- assign honors = site.data.awards | where: "highlight", true | where_exp: "a", "a.hidden != true" %}
{%- if honors.size > 0 %}
<div>
<h2 class="label">Honors</h2>
<ul class="dated wide">
{%- for a in honors %}
<li><span class="year">{% include when.html item=a %}</span><span>{{ a.name }}, {{ a.organization }}</span></li>
{%- endfor %}
</ul>
</div>
{%- endif %}
{%- if site.data.funders.size > 0 %}
<div>
<h2 class="label">Funding</h2>
<ul class="logos">
{%- for f in site.data.funders %}
{%- capture alt %}{{ f.name }}{% if f.full_name %} ({{ f.full_name }}){% endif %}{% endcapture %}
<li>{% if f.url %}<a href="{{ f.url }}">{% endif %}<img src="{{ f.logo | relative_url }}" alt="{{ alt | escape }}">{% if f.url %}</a>{% endif %}</li>
{%- endfor %}
</ul>
</div>
{%- endif %}
</section>
