---
name: Installation and use
anchor: installation-and-use
toc: 
 - name: Download and prepare files
   anchor: download-and-prepare-files
 - name: Configure your login information
   anchor: configure-your-login-information
 - name: Add overlay
   anchor: add-overlay
 - name: Starting WooferBot
   anchor: starting-wooferbot
---
This section explains installation process, broadcasting software setup and first run.

### Download and prepare files
1. Download and extract <a class="icon download" href="{{ site.github.latest_release.zipball_url }}">latest WooferBot release</a>.  
2. Download and extract <a class="icon download" href="{{ site.github.url }}/assets/files/python37.zip">Embedded Python 3.7</a> into WooferBot main directory.
3. Rename "settings.json.default" to "settings.json".

### Configure your login information
Edit settings.json file and change login information for your <a class="icon website" href="https://www.twitch.tv" target="_blank">twitch.tv</a> account. These parameters are **mandatory** for bot to work.
```
{
    "TwitchChannel": "",
    "TwitchOAUTH": ""
}
```
* <span class="icon settings">TwitchChannel</span> Channel name.
* <span class="icon settings">TwitchOAUTH</span> How to obtain a Twitch OAUTH: <a class="icon twitch" href="https://www.twitchapps.com/tmi/" target="_blank">www.twitchapps.com/tmi/</a>  
<br><span class="icon idea">Never share your Twitch OAUTH with anyone. If someone has seen your OAUTH, generate a new one as soon as possible.</span>

### Add overlay
Add <span class="icon file">overlay.html</span> as <a class="icon website" href="https://obsproject.com/wiki/Sources-Guide#browsersource" target="_blank">browser source</a> into your broadcasting software (<a class="icon website" href="https://obsproject.com" target="_blank">OBS</a>, etc...).

<span class="icon idea">Note: <a class="icon website" href="https://obsproject.com" target="_blank">OBS</a> seems to have an issue with "local file" option. If "local file" option does not work for you, open <span class="icon file">overlay.html</span> in your browser and copy URL instead.</span>
<br><span class="icon info">Recommended width: 1000px</span>
<br><span class="icon info">Recommended height: 500px</span>

**Best practices**
* Do not use "Shutdown source when not visible".
* Add WooferBot browser source into a dedicated scene.
* Add WooferBot scene into all other scenes.

<span class="icon idea">Note: This approach will prevent using multiple browser sources, which would require more system resources and cause possible conflicts or missed notifications.</span>

### Starting WooferBot
To start WooferBot execute <span class="icon file">wooferbot.cmd</span>.

To customize WooferBot, adjust "settings.json" as needed (see <a class="icon doc" href="{{ site.github.url }}/documentation#basic-configuration">Basic configuration</a> section).
