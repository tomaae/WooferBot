---
name: Updating from older version
anchor: updating-from-older-version
toc: 
 - name: Update WooferBot on windows
   anchor: update-wooferbot-on-windows
 - name: Update WooferBot on linux
   anchor: update-wooferbot-on-linux
---
This section explains how to update WooferBot to newest version.

### Update WooferBot on windows
1. Download and extract <a class="icon download" href="{{ site.github.url }}/changelog">latest WooferBot release</a> over previous version.
2. Start <span class="icon file">wooferbot_cli.exe</span> and close it after startup (This will add all new parameters into your configuration file and update any changes made between versions).
3. Update your configuration as needed to use new features.

### Update WooferBot on linux
1. Download and extract <a class="icon download" href="{{ site.github.url }}/changelog">latest WooferBot release</a> over previous version.
2. Go to wooferbot root directory
3. Install dependencies `python3 -m pipenv install`
4. Start `python3 -m pipenv run python3 wooferbot.py` and close it after startup (This will add all new parameters into your configuration file and update any changes made between versions).
5. Update your configuration as needed to use new features.
