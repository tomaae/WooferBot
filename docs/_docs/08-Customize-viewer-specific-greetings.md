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
    "CustomGreets": {
        "testname": [
            "Hello testname, welcome in."
        ]
    }
```

<br><span class="icon idea">Note: If not defined, default "greet" message will be used.</span>

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

