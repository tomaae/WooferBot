---
name: Create timed messages
anchor: create-timed-messages
toc: 
 - name: Configuring custom timers/scheduled messages
   anchor: configuring-custom-timersscheduled-messages
 - name: Mapping mascot poses to timed messages
   anchor: mapping-mascot-poses-to-timed-messages
---
This section explains how to create and edit timers.

### Configuring custom timers/scheduled messages
Allows you to schedule a message to appear every X minutes.

*Example:*
```
    "ScheduledMessages": [
        {
            "Name": "Twitter",
            "Timer": 30,
            "Enabled": 1,
            "Image": "twitterlogo.png",
            "Message": [
                "Check out my twitter @Tomaae_ for stream updates."
            ],
            "LastShown": 1544893802
        }
    ]
```
**List of parameters**
* <span class="icon settings">Name</span> Name of the Timer (Not shown on stream)
* <span class="icon settings">Timer</span> Timer in minutes
* <span class="icon settings">Enabled</span> (0/1)
* <span class="icon settings">Image</span> Optional image (has to be placed into "images" directory)
* <span class="icon settings">Message</span> Message shown on screen
* <span class="icon settings">LastShown</span> Internal parameter, do not modify

### Mapping mascot poses to timed messages
PoseMapping allows you to map available mascot poses to timed messages.
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
