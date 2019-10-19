---
shorttitle: Contacts
class: contacts
tags:
  - contact
  - contacts
  - discord
  - panels
  - panel
  - banners
  - banner
  - team
---
## Contacts

**Announcements, Support and Development updates available on Discord**

<a class="icon discord" href="https://discord.gg/vpprtdE" target="_blank">Discord</a><br>

**Feature request on Github**

<a class="icon github" href="https://github.com/tomaae/WooferBot/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature%5D" target="_blank">Suggest an idea</a>

**Bug report on Github**

<a class="icon github" href="https://github.com/tomaae/WooferBot/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBug%5D" target="_blank">Report an issue</a>

## Team
{% for member in site.team %}
### {{ member.name }}
<div class="mascot"><div>
<img src="{{ site.github.url }}/assets/images/team/{{ member.anchor }}.png">
</div><div><div>
{% if member.description %}
<b>Description:</b> {{ member.description }}<br>
{% if member.web -%}
<a class="icon website" href="{{ member.web }}" title="{{ member.web }}" target="_blank">{{ member.web }}</a><br>
{%- endif %}{% if member.twitter -%}
<a class="icon tweet" href="https://twitter.com/{{ member.twitter }}" target="_blank">@{{ member.twitter }}</a><br>
{%- endif %}{% if member.twitch -%}
<a class="icon twitch" href="https://www.twitch.tv/{{ member.twitch }}" target="_blank">{{ member.twitch }}</a><br>
{%- endif %}
{% endif %}
</div></div></div>
{% endfor %}

## Resources
Do you want a WooferBot panel for your twitch profile or website?
![Twitch Panel](/assets/images/panels/apricot.png)
![Twitch Panel](/assets/images/panels/beatrice.png)
![Twitch Panel](/assets/images/panels/cat-ragdoll.png)
![Twitch Panel](/assets/images/panels/cat-russian-blue.png)
![Twitch Panel](/assets/images/panels/cat-siamese.png)
![Twitch Panel](/assets/images/panels/cat-tabby.png)
![Twitch Panel](/assets/images/panels/lydia.png)
![Twitch Panel](/assets/images/panels/malamute.png)
![Twitch Panel](/assets/images/panels/mango.png)
![Twitch Panel](/assets/images/panels/nyuko.png)
![Twitch Panel](/assets/images/panels/tem.png)
