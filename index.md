---
layout: default
title: Home
---
{%- comment -%}
Home page. Profile links and the photo are set in _config.yml.
Selected publications are the entries in _data/publications.json with "selected": true.
HTML here is kept flush left so Markdown does not turn indented lines into code blocks.
{%- endcomment -%}
<section class="hero">
<div class="hero-text">
<h1>{{ site.author.name }}</h1>
<p class="position">{{ site.author.position }}</p>
<p class="statement">I compute the structure of atomic nuclei from nuclear forces, developing the in-medium similarity renormalization group to make ab initio predictions more precise and to quantify their uncertainties.</p>
<p class="links">
{%- if site.links.email != "" %}<a href="mailto:{{ site.links.email }}">Email</a>{% else %}<span class="placeholder">[email]</span>{% endif -%}
{%- if site.links.inspire != "" %}<a href="{{ site.links.inspire }}">INSPIRE</a>{% else %}<span class="placeholder">[INSPIRE link]</span>{% endif -%}
{%- if site.links.orcid != "" %}<a href="{{ site.links.orcid }}">ORCID</a>{% else %}<span class="placeholder">[ORCID link]</span>{% endif -%}
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
{%- assign selected = site.data.publications | where: "selected", true | sort: "year" | reverse %}
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
<li><span class="year">2026</span>FRIB Achievement Award for Early Career Researchers</li>
<li><span class="year">2024</span>Giersch Award for an Outstanding Doctoral Thesis</li>
<li><span class="year">2024</span>Gerhard Herzberg Research Prize</li>
<li><span class="year">2024</span>Wigner Distinguished Staff Fellowship, ORNL</li>
</ul>
</div>
<div>
<h2 class="label">Funding</h2>
<ul class="plain">
<li>[Agency — program, grant no.]</li>
<li>[Computing allocation — facility]</li>
</ul>
</div>
</section>
