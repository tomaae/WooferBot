---
name: Configure Philips Hue
anchor: configure-philips-hue
toc: 
 - name: Initial configuration
   anchor: initial-configuration
 - name: Configuring Philips Hue lights for mascot poses
   anchor: configuring-philips-hue-lights-for-mascot-poses
---
This section explains how to integrate your Philips Hue lights and use them for notifications.

### Initial configuration
Enable Philips Hue in the configuration file. IP will be automatically detected and quick setup will guide you and setup token.
```
{
    "HueEnabled": true,
    "HueIP": "10.0.0.1",
    "HueToken": "qwertyuiopasdfghjklzxcvbnm"
}
```
* <span class="icon settings">HueEnabled</span> (true/false) Enable/disable Philips Hue integration

<span class="icon idea">Note: Variables <span class="icon settings">HueIP</span> and <span class="icon settings">HueToken</span> are configured automatically.</span>

### Configuring Philips Hue lights for mascot poses
Add "Hue" variable into pose mapping and add all lights you want to use for each pose.
```
    "PoseMapping": {
        "follow": {
            "Image": "Wave",
            "Audio": "Wave",
            "Hue": {
            	"Hue lightstrip outdoor 1": {
            		"Brightness": 100,
            		"Color": "#b16a16"
            	},
            	"Hue color lamp 1": {
            		"Brightness": 100,
            		"Color": "#ff0000"
            	}
            },
            "HuePersistent": false
        }
    }
```

* <span class="icon settings">HuePersistent</span> (true/false) Apply light settings persistently. This will also replace Idle light mapping until bot is restarted.
* Light names ("Hue lightstrip outdoor 1", "Hue color lamp 1") are taken from Hue Bridge, see your Hue App.
* <span class="icon settings">Brightness</span> Light brightness (1-100)
* <span class="icon settings">Color</span> Colors are defined with hashtag, followed by 6-digit hexidecimal number. You can use web based <a class="icon website" href="https://www.w3schools.com/colors/colors_picker.asp" target="_blank">color picker</a> to choose or convert colors.