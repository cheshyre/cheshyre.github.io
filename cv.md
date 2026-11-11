---
layout: default
title: CV
permalink: /cv/
---
{%- comment -%}
The lists below come from _data/appointments.json, education.json, awards.json, funding.json, and
computing.json (copies of the CV data; see README.md). assets/cv.pdf is the full CV.
{%- endcomment -%}

# Curriculum vitae

[Download the full CV (PDF)]({{ '/assets/cv.pdf' | relative_url }})

## Education

<ul class="dated wide">
{%- for e in site.data.education %}
<li><span class="year">{% include when.html item=e %}</span><span>{{ e.degree }}, {{ e.institution }}</span></li>
{%- endfor %}
</ul>

## Appointments

<ul class="dated wide">
{%- for a in site.data.appointments %}
<li><span class="year">{% include when.html item=a %}</span><span>{{ a.title }}, {{ a.institution }}</span></li>
{%- endfor %}
</ul>

## Fellowships and awards

<ul class="dated wide">
{%- assign awards = site.data.awards | where_exp: "a", "a.hidden != true" %}
{%- for a in awards %}
<li><span class="year">{% include when.html item=a %}</span><span>{{ a.name }}, {{ a.organization }}</span></li>
{%- endfor %}
</ul>

## Funding

<ul class="dated wide">
{%- for f in site.data.funding %}
<li><span class="year">{% include when.html item=f %}</span><span>{{ f.title }}{% if f.role %} ({{ f.role }}){% elsif f.pi %} (PI: {{ f.pi }}){% endif %}{% if f.amount_usd %}, ${% include thousands.html n=f.amount_usd %}{% endif %}</span></li>
{%- endfor %}
</ul>

## Computing grants

<ul class="dated wide">
{%- for c in site.data.computing %}
{%- assign alloc = c.allocations | first %}
<li><span class="year">{% include when.html item=c %}</span><span>{{ c.resource }} ({% if c.program %}{{ c.program }} {% endif %}project {{ c.project }})
{%- if alloc.cpu_core_hours %}: CPU {{ alloc.cpu_core_hours | divided_by: 100000.0 | round | divided_by: 10.0 }}M core-h{% endif %}
{%- if alloc.gpu_core_hours %}, GPU {{ alloc.gpu_core_hours | divided_by: 100000.0 | round | divided_by: 10.0 }}M core-h{% endif %}
{%- if alloc.year %} ({{ alloc.year }}){% endif %}</span></li>
{%- endfor %}
</ul>

Publications and talks are listed on the [Publications]({{ '/publications/' | relative_url }}) page; lectures and students are on the [Teaching]({{ '/teaching/' | relative_url }}) page.
