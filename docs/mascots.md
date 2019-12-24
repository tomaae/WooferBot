---
shorttitle: Mascots
title: WooferBot, visual bot for streamers
description: >
  WooferBot is fully customizable interactive mascot for streamers, designed to be 
  used as Browser Source within broadcasting software.
class: mascots
tags:
  - Mascots
  - Avatars
---
<div class="heading">
    <span><svg><text x="50%" y="40px">MASCOTS</text></svg></span><br>
    <span><a href="javascript:mascotFilter('all')">ALL</a><img src="assets/images/paw-sr.png"><a href="javascript:mascotFilter('humanoid')">HUMAN, HUMANOID</a><img src="assets/images/paw-sr.png"><a href="javascript:mascotFilter('animal')">ANIMAL, CREATURE</a></span><br>
    <span>Want to create your own mascot? Check out our <a class="icon doc" href="{{ site.github.url }}/documentation#creating-a-mascot">documentation</a> or<br>contact us on <a class="icon discord" href="https://discord.gg/vpprtdE" target="_blank">discord</a> and we'll help you sort it out.</span>
</div>
<div>
<div id="f_humanoid"><span class="caption">HUMAN, HUMANOID</span>
{% for mascot in site.mascots_human %}
<div class="list_m" id="m_{{ mascot.anchor }}" onmouseover="mascotHover('{{ mascot.anchor }}')" onmouseout="mascotUnhover('{{ mascot.anchor }}')">
    <div><img src="{{ site.github.url }}/assets/images/mascots/{{ mascot.anchor }}.png"></div>
    <div>
        <div>{{ mascot.name }}</div>
        <div><span>{{ mascot.type }}</span>{% if mascot.vo %}<span id="BTN"><div class="arrow_l" onmousedown="mascotART('{{ mascot.anchor }}')"></div><div class="arrow_r" onmousedown="mascotVA('{{ mascot.anchor }}')"></div></span>{% endif %}</div>
<div id="ART"><span>Artist</span> - {{ mascot.artist }}
{% if mascot.artist_web -%}
<br><a class="icon website" href="{{ mascot.artist_web }}" target="_blank">{{ mascot.artist_web }}</a>
{%- endif %}{% if mascot.artist_twitter -%}
<br><a class="icon tweet" href="https://twitter.com/{{ mascot.artist_twitter }}" target="_blank">@{{ mascot.artist_twitter }}</a>
{%- endif %}{% if mascot.artist_twitch -%}
<br><a class="icon twitch" href="https://www.twitch.tv/{{ mascot.artist_twitch }}" target="_blank">{{ mascot.artist_twitch }}</a>
{%- endif %}
</div>
{% if mascot.vo %}
<div id="VA"><span>Voice Actor</span> - {{ mascot.vo }}
{% if mascot.vo_web -%}
<br><a class="icon website" href="{{ mascot.vo_web }}" target="_blank">{{ mascot.vo_web }}</a>
{%- endif %}{% if mascot.vo_twitter -%}
<br><a class="icon tweet" href="https://twitter.com/{{ mascot.vo_twitter }}" target="_blank">@{{ mascot.vo_twitter }}</a>
{%- endif %}{% if mascot.vo_twitch -%}
<br><a class="icon twitch" href="https://www.twitch.tv/{{ mascot.vo_twitch }}" target="_blank">{{ mascot.vo_twitch }}</a>
{%- endif %}
</div>
{% endif %}
</div>
</div>
{% endfor %}
</div>
<div id="f_animal"><span class="caption">ANIMAL, CREATURE</span>
{% for mascot in site.mascots_animal %}
<div class="list_m" id="m_{{ mascot.anchor }}" onmouseover="mascotHover('{{ mascot.anchor }}')" onmouseout="mascotUnhover('{{ mascot.anchor }}')">
    <div><img src="{{ site.github.url }}/assets/images/mascots/{{ mascot.anchor }}.png"></div>
    <div>
        <div>{{ mascot.name }}</div>
        <div><span>{{ mascot.type }}</span>{% if mascot.vo %}<span id="BTN"><div class="arrow_l" onmousedown="mascotART('{{ mascot.anchor }}')"></div><div class="arrow_r" onmousedown="mascotVA('{{ mascot.anchor }}')"></div></span>{% endif %}</div>
<div id="ART"><span>Artist</span> - {{ mascot.artist }}
{% if mascot.artist_web -%}
<br><a class="icon website" href="{{ mascot.artist_web }}" target="_blank">{{ mascot.artist_web }}</a>
{%- endif %}{% if mascot.artist_twitter -%}
<br><a class="icon tweet" href="https://twitter.com/{{ mascot.artist_twitter }}" target="_blank">@{{ mascot.artist_twitter }}</a>
{%- endif %}{% if mascot.artist_twitch -%}
<br><a class="icon twitch" href="https://www.twitch.tv/{{ mascot.artist_twitch }}" target="_blank">{{ mascot.artist_twitch }}</a>
{%- endif %}
</div>
{% if mascot.vo %}
<div id="VA"><span>Voice Actor</span> - {{ mascot.vo }}
{% if mascot.vo_web -%}
<br><a class="icon website" href="{{ mascot.vo_web }}" target="_blank">{{ mascot.vo_web }}</a>
{%- endif %}{% if mascot.vo_twitter -%}
<br><a class="icon tweet" href="https://twitter.com/{{ mascot.vo_twitter }}" target="_blank">@{{ mascot.vo_twitter }}</a>
{%- endif %}{% if mascot.vo_twitch -%}
<br><a class="icon twitch" href="https://www.twitch.tv/{{ mascot.vo_twitch }}" target="_blank">{{ mascot.vo_twitch }}</a>
{%- endif %}
</div>
{% endif %}
</div>
</div>
{% endfor %}
</div>
</div>