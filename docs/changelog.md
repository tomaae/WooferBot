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
## Changelog and Release News

These are the latest versions of WooferBot which have been released.
{% for release in site.github.releases limit:5 %}

## [{{ release.name }}]({{ release.html_url }}) {% if release.prerelease -%}(pre-release){%- endif %}
Released <time datetime="{{ release.published_at | date_to_xmlschema }}">{{ release.published_at | date_to_string }}</time>

{{ release.body }}

### Assets
<ul class="btnlist">
<li><a class="buttons download" href="{{ release.zipball_url }}">Download release</a></li>
<li><a class="buttons download" href="{{ site.github.url }}/assets/files/python37.zip">Download Embedded Python 3.7</a></li>
{% for asset in release.assets -%}
<li><a class="buttons download" href="{{ asset.browser_download_url }}">{{ asset.name }}</a></li>
{%- endfor %}
</ul>
{% endfor %}
