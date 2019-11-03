---
name: Create watchdog trigger
anchor: create-watchdog-trigger
toc: 
 - name: Configuring custom watchdog trigers
   anchor: configuring-custom-watchdog-trigers
 - name: Mapping mascot poses to watchdog triggers
   anchor: mapping-mascot-poses-to-watchdog-triggers
---
This section explains how to create and edit watchdog triggers.

### Configuring custom watchdog trigers
Allows you to watch file for changes and trigger a notification.

<br>
*Example:*
```
    "Watchdog": [
        {
            "Name": "Now Playing",
            "Filename": "d:\\streaming\\now_playing.txt",
            "Enabled": true,
            "Command": "",
            "Message": "Now Playing: ",
            "Image": ""
        }
    ]
```
**List of parameters**
* <span class="icon settings">Name</span> Name of the watchdog trigger (Not shown on stream)
* <span class="icon settings">Filename</span> Filename to watch for changes
* <span class="icon settings">Enabled</span> (true/false)
* <span class="icon settings">Command</span> Name of a custom command. This will execute custom command (Image and Message values in this scheduled message will be ignored).
* <span class="icon settings">Message</span> Message to be prepended to the file content
* <span class="icon settings">Image</span> Optional image (has to be placed into "images" directory)

<span class="icon idea">Note: Always use double backslash in <span class="icon settings">Filename</span>.</span>

### Mapping mascot poses to watchdog triggers
PoseMapping allows you to map available mascot poses to watchdog triggers.
All notification and commands will use DEFAULT mapping unless a mapping is created for them.
```
    "PoseMapping": {
        "DEFAULT": {
            "Image": "Wave",
            "Audio": "Wave"
        },
        "Twitter": {
            "Image": "Happy",
            "Audio": "Happy"
        }
    }
```
