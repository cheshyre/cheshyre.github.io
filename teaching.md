---
layout: default
title: Teaching
permalink: /teaching/
---
{%- comment -%}
Lectures come from _data/lectures.json and students from _data/students.json (copies of the CV
data; see README.md), in file order.
{%- endcomment -%}

# Teaching and mentoring

## Lectures at physics schools

{% assign months = "January,February,March,April,May,June,July,August,September,October,November,December" | split: "," -%}
{%- assign words = "zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve" | split: "," -%}
<div class="pubs">
{%- for l in site.data.lectures %}
{%- assign parts = l.date | split: "-" %}
{%- assign m = parts[1] | plus: 0 | minus: 1 %}
{%- capture what -%}
{%- if l.lectures -%}{{ words[l.lectures.count] | default: l.lectures.count | capitalize }} {{ l.lectures.minutes }}-minute {% if l.lectures.kind %}{{ l.lectures.kind }} {% endif %}lecture{% if l.lectures.count != 1 %}s{% endif %}{%- endif -%}
{%- if l.exercises %} and {{ words[l.exercises.count] | default: l.exercises.count }} {{ l.exercises.minutes }}-minute {% if l.exercises.kind %}{{ l.exercises.kind }} {% endif %}exercise{% if l.exercises.count != 1 %}s{% endif %}{%- endif -%}
{%- endcapture %}
<div class="pub">
<span class="pub-year">{{ parts[0] }}</span>
<div>
<p class="pub-title">{{ l.topic }}</p>
<p class="pub-meta">{{ l.name }}, {{ l.location }} · <span class="nowrap">{% if parts[1] %}{{ months[m] }} {% endif %}{{ parts[0] }}</span> · {{ what }}</p>
</div>
</div>
{%- endfor %}
</div>

## Students advised

<ul class="plain">
{%- for s in site.data.students %}
{%- capture detail -%}
{%- if s.ongoing -%}ongoing
{%- elsif s.theses -%}{%- for t in s.theses -%}{{ t.degree }} {{ t.date }}{% unless forloop.last %}, {% endunless %}{%- endfor -%}
{%- elsif s.program -%}{{ s.program }} {{ s.date }}
{%- else -%}{{ s.date }}
{%- endif -%}
{%- endcapture %}
<li>{{ s.name }}{% if detail != "" %} ({{ detail }}){% endif %}</li>
{%- endfor %}
</ul>
