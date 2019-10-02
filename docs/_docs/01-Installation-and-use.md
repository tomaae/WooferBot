---
name: Installation and use
anchor: installation-and-use
toc: 
 - name: Installation
   anchor: installation
 - name: Add overlay
   anchor: add-overlay
 - name: Starting WooferBot
   anchor: starting-wooferbot
---
This section explains installation process, broadcasting software setup and first run.

### Installation
1. Download and extract <a class="icon download" href="{{ site.github.latest_release.zipball_url }}">latest WooferBot release</a>.  
2. Download and extract <a class="icon download" href="{{ site.github.url }}/assets/files/python37.zip">Embedded Python 3.7</a> into WooferBot main directory.
3. Rename "settings.json.default" to "settings.json".
4. Customize "settings.json" as needed (see <a class="icon doc" href="{{ site.github.url }}/documentation#basic-configuration">Basic configuration</a> section).

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
