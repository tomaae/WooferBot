---
shorttitle: Changelog
title: Changelog and Release News
description: >
  Detailed changelog and news for the WooferBot releases including
  links to compare the code differences between the last seven released
  versions.
class: changelog
tags:
  - changelog
  - news
  - changes
  - release
  - releases
  - installer
---
<div class="heading">
	<span><svg><text x="50%" y="40px">CHANGELOG AND RELEASE NEWS</text></svg></span><br>
	<span>You can find latest versions of WooferBot here.</span>
	<span></span>
</div>
{% for release in site.github.releases limit:5 %}
<div class="caption"><span>{{ release.name }}{% if release.prerelease -%} (pre-release){%- endif %}</span><span>Release date: <time datetime="{{ release.published_at | date_to_xmlschema }}">{{ release.published_at | date_to_string }}</time></span></div>
{{ release.body }}
<div class="dllist">
	<a href="{{ release.zipball_url }}"><span>Download release</span></a>
	<a href="{{ site.github.url }}/assets/files/python37.zip"><span>Download Embedded Python 3.7</span></a>
{% for asset in release.assets -%}
<a href="{{ asset.browser_download_url }}"><span>{{ asset.name }}</span></a>
{%- endfor %}
</div>
<img class="pawsep" src="{{ site.github.url }}/assets/images/paw-separator.png">
{% endfor %}