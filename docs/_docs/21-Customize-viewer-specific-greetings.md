---
name: Customize viewer specific greetings
anchor: customize-viewer-specific-greetings
toc: 
 - name: Create viewer specific greeting messages
   anchor: create-viewer-specific-greeting-messages
 - name: Create viewer specific greeting pose mapping
   anchor: create-viewer-specific-greeting-pose-mapping
---
This section explains how to further customize viewer notifications.

### Create viewer specific greeting messages
You can define special greeting message for any viewer.
It is possible to define multiple replies for each message and have bot pick one at random.

*Example:*
```
    "Messages": {
        "viewer_testname": [
            "[Hello;Hi;Hey;Hewwo;Ello] {sender}, can I have some treats please?",
            "[Hello;Hi;Hey;Hewwo;Ello] {sender}!? Are you here to pet me? Or to give me wet food? Either one is fine, just let me know! ^..^"
        ]
    }
```

<br><span class="icon idea">Note: If not defined, default "greet" message will be used.</span>
<br><span class="icon info">For more information about messages, see <a class="icon doc" href="{{ site.github.url }}/documentation#customize-notifications-and-commands">Customize notifications and commands</a>.</span>

### Create viewer specific greeting pose mapping
You can map a separate post for special greeting for any viewer.
Notification will be mapped to "greet" if not defined.

*Example:*
```
    "PoseMapping": {
        "viewer_testname": {
            "Image": "Wave",
            "Audio": "Wave"
        }
    }
```

<br><span class="icon idea">Note: If not defined, default "greet" pose mapping will be used.</span>
<br><span class="icon idea">Note: You have to use "viewer_" prefix for special greeting pose mapping.</span>

