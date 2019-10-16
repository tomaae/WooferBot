---
name: Create custom commands
anchor: create-custom-commands
toc: 
 - name: Configuring custom commands
   anchor: configuring-custom-commands
 - name: Mapping mascot poses to custom commands
   anchor: mapping-mascot-poses-to-custom-commands
---
This section explains how to create custom commands.


### Configuring custom commands
You can create simple custom replies using "Commands".

*Example:*
```
    "Commands": {
        "!hello": {
            "Message": [
                "[Hello;Hi;Hey;Hewwo;Ello] {sender} :3"
            ],
            "Image" : "",
            "Script" : "",
            "Enabled": true,
            "ViewerOnce": false,
            "ViewerTimeout": 0,
            "GlobalTimeout": 0,
            "Access" : ""
        }
    }
```
**List of parameters**
* <span class="icon settings">Message</span> Message shown on screen
* <span class="icon settings">Image</span> Optional image (has to be placed into "images" directory)
* <span class="icon settings">Script</span> Execute a script (has to be placed into "scripts" directory)
* <span class="icon settings">Access</span>
  * "" - Everyone can use the command if left empty
  * "mod" - Only mods or broadcaster can use the commands
  * "broadcasted" - Only broadcaster can use the commands
* <span class="icon settings">ViewerOnce</span> (true/false) Command can be used only once per viewer during a session.
* <span class="icon settings">ViewerTimeout</span> Command can be used only once per viewer within X number of seconds (0 - disabled).
* <span class="icon settings">GlobalTimeout</span> Command can be used only once within X number of seconds (0 - disabled).
* <span class="icon settings">Enabled</span> (true/false)

### Mapping mascot poses to custom commands
PoseMapping allows you to map available mascot poses to your custom commands.
All notification and commands will use DEFAULT mapping unless a mapping is created for them.
```
    "PoseMapping": {
        "DEFAULT": {
            "Image": "Wave",
            "Audio": "Wave"
        },
        "!hello": {
            "Image": "Happy",
            "Audio": "Happy"
        }
    }
```
