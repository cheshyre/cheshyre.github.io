---
layout: default
title: Home
---
{%- comment -%}
Home page. Position, profile links, and the photo are set in _config.yml.
Selected publications are the entries in _data/publications.json with "selected": true, in file order.
Honors are the first four visible entries of _data/awards.json; Funding lists the current entries of
_data/funding.json and _data/computing.json (those ending this year or later, or ongoing).
HTML here is kept flush left so Markdown does not turn indented lines into code blocks.
{%- endcomment -%}
<section class="hero">
<div class="hero-text">
<h1>{{ site.author.name }}</h1>
<p class="position">{{ site.author.position }}</p>
{%- if site.author.previously %}
<p class="previously">Previously {{ site.author.previously }}</p>
{%- endif %}
<p class="statement">I compute the structure of atomic nuclei from nuclear forces, developing the in-medium similarity renormalization group to make ab initio predictions more precise and to quantify their uncertainties.</p>
<p class="links">
{%- if site.links.email != "" %}<a href="mailto:{{ site.links.email }}">Email</a>{% else %}<span class="placeholder">[email]</span>{% endif -%}
{%- if site.links.inspire != "" %}<a href="{{ site.links.inspire }}">INSPIRE</a>{% else %}<span class="placeholder">[INSPIRE link]</span>{% endif -%}
{%- if site.links.orcid != "" %}<a href="{{ site.links.orcid }}">ORCID</a>{% else %}<span class="placeholder">[ORCID link]</span>{% endif -%}
{%- if site.links.scholar and site.links.scholar != "" %}<a href="{{ site.links.scholar }}">Google Scholar</a>{% endif -%}
{%- if site.links.github != "" %}<a href="{{ site.links.github }}">GitHub</a>{% endif -%}
</p>
</div>
{%- if site.photo != "" %}
<img class="photo" src="{{ site.photo | relative_url }}" alt="Portrait of {{ site.author.name }}" width="176" height="176">
{%- else %}
<div class="photo" role="img" aria-label="Portrait placeholder">[Photo]</div>
{%- endif %}
</section>

<section class="section">
<h2 class="label">Research interests</h2>
<div class="grid-2">
<div><p class="item-title">Precision many-body methods</p><p class="item-text">IMSRG(3) and controlled estimates of many-body uncertainties.</p></div>
<div><p class="item-title">Heavy and neutron-rich nuclei</p><p class="item-text">Shell structure, charge radii, and neutron skins.</p></div>
<div><p class="item-title">Physics beyond the Standard Model</p><p class="item-text">Nuclear matrix elements for dark matter and symmetry tests.</p></div>
<div><p class="item-title">Computing for nuclear theory</p><p class="item-text">Quantum algorithms and GPU-scale simulations.</p></div>
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
<h2 class="label">Honors</h2>
<ul class="dated">
{%- assign honors = site.data.awards | where_exp: "a", "a.hidden != true" %}
{%- for a in honors limit: 4 %}
<li><span class="year">{% include when.html item=a start_only=true %}</span><span>{{ a.name }}, {{ a.organization }}</span></li>
{%- endfor %}
</ul>
</div>
<div>
<h2 class="label">Funding</h2>
<ul class="plain">
{%- assign this_year = site.time | date: "%Y" | plus: 0 %}
{%- for f in site.data.funding %}
{%- assign until = f.end | default: f.date %}
{%- assign until_year = until | slice: 0, 4 | plus: 0 %}
{%- if until == nil or until_year >= this_year %}
<li>{{ f.title }}{% if f.role %} ({{ f.role }}){% elsif f.pi %} (PI: {{ f.pi }}){% endif %}, <span class="nowrap">{% include when.html item=f %}</span></li>
{%- endif %}
{%- endfor %}
{%- for c in site.data.computing %}
{%- assign until = c.end | default: c.date %}
{%- assign until_year = until | slice: 0, 4 | plus: 0 %}
{%- if until == nil or until_year >= this_year %}
<li>Computing grant: {{ c.resource }} ({% if c.program %}{{ c.program }} {% endif %}project {{ c.project }}), <span class="nowrap">{% include when.html item=c %}</span></li>
{%- endif %}
{%- endfor %}
</ul>
</div>
</section>
