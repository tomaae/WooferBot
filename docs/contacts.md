---
shorttitle: Contacts
title: WooferBot, visual bot for streamers
description: >
  WooferBot is fully customizable interactive mascot for streamers, designed to be 
  used as Browser Source within broadcasting software.
class: contacts
tags:
  - contact
  - contacts
  - discord
  - team
---
<div class="heading">
    <span><svg><text x="50%" y="40px">CONTACTS</text></svg></span><br>
    <span></span>
    <span></span>
</div>
<div>
    <div>
        <a href="https://discord.gg/vpprtdE" target="_blank">
        <div class="contact">
            <div><img src="assets/images/icons/discord-mw.png"></div>
            <div>
                <div>JOIN OUR DISCORD SERVER</div>
                <div>Announcements, Support and Development updates</div>
            </div>
        </div>
        </a>
        <a href="https://github.com/tomaae/WooferBot/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature%5D" target="_blank">
        <div class="contact">
            <div><img src="assets/images/icons/github-mw.png"></div>
            <div>
                <div>FEATURE REQUEST</div>
                <div>Suggest an idea on Github</div>
            </div>
        </div>
        </a>
        <a href="https://github.com/tomaae/WooferBot/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBug%5D" target="_blank">
        <div class="contact">
            <div><img src="assets/images/icons/github-mw.png"></div>
            <div>
                <div>BUG REPORT</div>
                <div>Report an issue on Github</div>
            </div>
        </div>
        </a>
    </div>
    <div class="team"><span class="caption">TEAM</span>

{% for member in site.team %}
<div class="list_t">
    <div><img src="{{ site.github.url }}/assets/images/team/{{ member.anchor }}.png"></div>
    <div>
        <div>{{ member.name }}</div>
        <div>{% if member.description %}<span>{{ member.description }}</span>{% endif %}</div>
        <div>
{% if member.web -%}
<a class="icon website" href="{{ member.web }}" title="{{ member.web }}" target="_blank">{{ member.web }}</a><br>
{%- endif %}{% if member.twitter -%}
<a class="icon tweet" href="https://twitter.com/{{ member.twitter }}" target="_blank">@{{ member.twitter }}</a><br>
{%- endif %}{% if member.twitch -%}
<a class="icon twitch" href="https://www.twitch.tv/{{ member.twitch }}" target="_blank">{{ member.twitch }}</a><br>
{%- endif %}
</div></div></div>
{% endfor %}

</div></div>