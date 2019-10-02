---
shorttitle: Documentation
title: WooferBot Documentation
class: documentation
tags:
  - documentation
  - installation
  - configure
  - setup
---
## WooferBot Documentation

## Table of content
{% for doc in site.docs %}
- [{{ doc.name }}]({{ site.github.url }}/documentation#{{ doc.anchor }}){% if doc.toc %}{% for toc in doc.toc %}
  - [{{ toc.name }}]({{ site.github.url }}/documentation#{{ toc.anchor }}){% endfor %}{% endif %}{% endfor %}


{% for doc in site.docs %}
---
## {{ doc.name }}
{{ doc.content }}
{% endfor %}
