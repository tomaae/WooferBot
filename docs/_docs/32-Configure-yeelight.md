---
name: Configure Yeelight
anchor: configure-yeelight
toc: 
 - name: Initial configuration
   anchor: initial-configuration
 - name: Configuring Yeelight lights for mascot poses
   anchor: configuring-yeelight-lights-for-mascot-poses
---
This section explains how to integrate your Yeelight lights and use them for notifications.

### Initial configuration
<a class="icon website" href="https://www.yeelight.com/faqs/lan_control" target="_blank">Enable LAN Control</a> for each Yeelight device you want to control using Yeelight APP.

Enable Yeelight in the configuration file.
```
{
    "YeelightEnabled": true
}
```
* <span class="icon settings">YeelightEnabled</span> (true/false) Enable/disable Yeelight integration

<span class="icon idea">Note: You will have to name all your Yeelight lights during first run.</span>

### Configuring Yeelight lights for mascot poses
Add "Yeelight" variable into pose mapping and add all lights you want to use for each pose.
```
    "PoseMapping": {
        "follow": {
            "Image": "Wave",
            "Audio": "Wave",
            "Yeelight": {
                "Yeelight Lightstrip 1": {
                    "Brightness": 50,
                    "Color": "#0000ff",
                    "Transition": true,
                    "TransitionTime": 1000
                }
            },
            "YeelightPersistent": true
        }
    }
```

* Light names ("Yeelight Lightstrip 1", "Yeelight color lamp 1") are set up during first run after enabling Yeelight in WooferBot.
* <span class="icon settings">Brightness</span> Light brightness (1-100)
* <span class="icon settings">Color</span> Colors are defined with hashtag, followed by 6-digit hexidecimal number. You can use web based <a class="icon website" href="https://www.w3schools.com/colors/colors_picker.asp" target="_blank">color picker</a> to choose or convert colors.
* <span class="icon settings">Transition</span> (true/false) Enable transition between colors. When disabled, transition will be instant.
* <span class="icon settings">TransitionTime</span> Transition duration in miliseconds
* <span class="icon settings">YeelightPersistent</span> (true/false) Apply light settings persistently. This will also replace Idle light mapping until bot is restarted.
