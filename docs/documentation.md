---
shorttitle: Documentation
title: WooferBot Documentation
class: doc
tags:
  - documentation
  - installation
  - configure
  - setup
---
<div class="heading">
    <span><svg><text x="50%" y="40px">DOCUMENTATION</text></svg></span><br>
    <span></span>
    <span></span>
</div>

## TABLE OF CONTENT
{% for doc in site.docs %}
- [{{ doc.name }}]({{ site.github.url }}/documentation#{{ doc.anchor }}){% if doc.toc %}{% for toc in doc.toc %}
  - [{{ toc.name }}]({{ site.github.url }}/documentation#{{ toc.anchor }}){% endfor %}{% endif %}{% endfor %}

<img class="pawsep" src="{{ site.github.url }}/assets/images/paw-separator.png">

{% for doc in site.docs %}
## {{ doc.name }}
{{ doc.content }}
<img class="pawsep" src="{{ site.github.url }}/assets/images/paw-separator.png">
{% endfor %}
