---
name: Configure nanoleaf
anchor: configure-nanoleaf
toc: 
 - name: Initial configuration
   anchor: initial-configuration
 - name: Setting Nanoleaf motions for mascot poses
   anchor: setting-nanoleaf-motions-for-mascot-poses
---
This section explains how to integrate Nanoleaf and use light scenes for notifications.

### Initial configuration
Enable Nanoleaf in the configuration file. IP will be automatically detected and quick setup will guide you and setup token.
```
{
    "NanoleafEnabled": true,
    "NanoleafIP": "10.0.0.1",
    "NanoleafToken": "qwertyuiopasdfghjklzxcvbnm"
}
```
* <span class="icon settings">NanoleafEnabled</span> Enable nanoleaf integration: true/false

<span class="icon idea">Note: Variables <span class="icon settings">NanoleafIP</span> and <span class="icon settings">NanoleafToken</span> are configured automatically.</span>

### Setting Nanoleaf motions for mascot poses
Add "Nanoleaf" variable into pose mapping and enter Nanoleaf motion as its value.
```
    "PoseMapping": {
        "follow": {
            "Image": "Wave",
            "Audio": "Wave",
            "Nanoleaf": "Nemo"
        },
        "sub": {
            "Image": "Sub",
            "Audio": "Sub",
            "Nanoleaf": "Orange Beat"
        }
    }
```
