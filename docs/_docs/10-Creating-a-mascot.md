---
name: Creating a mascot
anchor: creating-a-mascot
toc: 
 - name: Mascot images
   anchor: mascot-images
 - name: Directory structure
   anchor: directory-structure
 - name: Configure mascot
   anchor: configure-mascot
---
This section provides guidelines and explains how to create custom mascots.

### Mascot images
For smooth looking transitions, all mascot images should follow these guidelines:
* All images should have identical image width and height
* Mascot should be centered vertically in the image
* Mascot's "feet" should be at same position from bottom

Recommended poses:
* Default idle pose
* Greeting pose (commonly used for greeting new chatters)
* Happy pose (commonly used for hosts, raids and shoutouts)
* Excited (for humanoid)/Snacking(for animal) pose (commonly used for subs and bits)

### Directory structure
1. Create a subdirectory within "Mascots" directory with the name of your mascot.
2. Create following subdirectories within your mascot directory: "images", "audio"
3. Create an empty configuration file within your mascot directory: "mascot.json"

*Example directory structure:*
```
\mascots\mymascot\
\mascots\mymascot\audio\
\mascots\mymascot\images\
\mascots\mymascot\mascot.json
```

### Configure mascot
Mascot configuration file is used to map mascot pose names to custom images and their parameters.

Example:
```
{
    "mascotImages": {
        "Idle": {
            "Image": "idle.png"
        },
        "Wave": {
            "Image": "wave.png",
            "MouthHeight": 87,
            "Time": 5000
        },
        "Happy": {
            "Image": "happy.png",
            "MouthHeight": 95,
            "Time": 7000
        },
        "Snack": {
            "Image": "snack.png",
            "MouthHeight": 90,
            "Time": 7000
        }
    },
    "mascotAudio": {
        "Wave": {
            "Audio": ["hi.mp3", "hello.mp3"],
            "Volume": 0.2
        },
        "Happy": {
            "Audio": ["happy.mp3"],
            "Volume": 0.2
        },
        "Snack": {
            "Audio": ["nom.mp3"],
            "Volume": 0.2
        }
    },
    "mascotStyles": {
        "MascotMaxWidth": 150
    }
}
```
<span class="icon idea">Note: Configuration parameters are case sensitive. Changing parameter case will break them. Change only values or pose names.</span>
<span class="icon idea">Note: JSON format requires comma to be present after every parameter within a block, except at the end (before closing curly brackets).</span>

**Pose naming rules and recommendations**
* Definition of "Idle" pose is mandatory
* Definition of "Wave" pose and audio is recommended (used as default)
* First letter of a pose name has to be capitalized
* It is recommended to follow the list of pose names for easier mascot setup
* You can also create additional poses with custom names
* Custom Images and Audio pose names do not have to match

**List of recommended poses**
* Idle
* Wave
* Happy
* Snack

**List of image parameters**
* <span class="icon settings">Image</span> Image file name (preferred: png for static, gif for animated)
* <span class="icon settings">MouthHeight</span> Height of mascot's mouth in this image. Message bubble arrow will be set to this height.
* <span class="icon settings">Time</span> Duration in miliseconds (also used for timing in case of animated files)

**List of audio parameters**
* <span class="icon settings">Audio</span> Audio file name (preferred: mp3)
* <span class="icon settings">Volume</span> Audio volume level 0-1 (Accepts decimal values)

**List of styles**
* <span class="icon settings">MascotMaxWidth</span> Width of widest pose image
