---
shorttitle: Mascots
class: mascots
tags:
  - Mascots
  - Avatars
---
## WooferBot Mascots
## Table of content
{% for mascot in site.mascots %}
* [{{ mascot.name }}]({{ site.github.url }}/mascots#{{ mascot.anchor }}){% endfor %}


{% for mascot in site.mascots %}
## {{ mascot.name }}
<div class="mascot"><div>
<img src="{{ site.github.url }}/assets/images/mascots/{{ mascot.anchor }}.png">
</div><div><div>
{% if mascot.artist %}
<b>Artist:</b> {{ mascot.artist }}<br>
{% if mascot.artist_web -%}
<a class="icon website" href="{{ mascot.artist_web }}" title="{{ mascot.artist_web }}" target="_blank">{{ mascot.artist_web }}</a><br>
{%- endif %}{% if mascot.artist_twitter -%}
<a class="icon tweet" href="https://twitter.com/{{ mascot.artist_twitter }}" target="_blank">@{{ mascot.artist_twitter }}</a><br>
{%- endif %}{% if mascot.artist_twitch -%}
<a class="icon twitch" href="https://www.twitch.tv/{{ mascot.artist_twitch }}" target="_blank">{{ mascot.artist_twitch }}</a><br>
{%- endif %}
{% endif %}
</div><div>
{% if mascot.vo %}
<b>Voice Actor:</b> {{ mascot.vo }}<br>
{% if mascot.vo_web -%}
<a class="icon website" href="{{ mascot.vo_web }}" title="{{ mascot.vo_web }}" target="_blank">{{ mascot.vo_web }}</a><br>
{%- endif %}{% if mascot.vo_twitter -%}
<a class="icon tweet" href="https://twitter.com/{{ mascot.vo_twitter }}" target="_blank">@{{ mascot.vo_twitter }}</a><br>
{%- endif %}{% if mascot.vo_twitch -%}
<a class="icon twitch" href="https://www.twitch.tv/{{ mascot.vo_twitch }}" target="_blank">{{ mascot.vo_twitch }}</a><br>
{%- endif %}
{% endif %}
</div></div></div>
{% endfor %}
