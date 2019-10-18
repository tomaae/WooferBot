---
name: Customize notifications and commands
anchor: customize-notifications-and-commands
toc: 
 - name: Customize notifications and commands
   anchor: customize-notifications-and-commands
 - name: Customize user activities
   anchor: customize-user-activities
 - name: Enabling/Disabling notifications and commands
   anchor: enablingdisabling-notifications-and-commands
 - name: Mapping mascot poses to notifications
   anchor: mapping-mascot-poses-to-notifications
 - name: List of predefined notification and commands
   anchor: list-of-predefined-notification-and-commands
---
This section explains how to customize notifications, add custom commands and timers.

### Customize notifications and commands
"Messages" are used to customize replies to default notifications and commands.
It is possible to define multiple replies for each message and have bot pick one at random.

*Example:*
```
    "Messages": {
        "greet": [
            "[Hello;Hi;Hey;Hewwo;Ello] {sender}, can I have some treats please?",
            "[Hello;Hi;Hey;Hewwo;Ello] {sender}!? Are you here to pet me? Or to give me wet food? Either one is fine, just let me know! ^..^"
        ],
        "sub": [
            "[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for becoming our best friend ^..^"
        ]
    }
```
<span class="icon info">See <a class="icon doc" href="{{ site.github.url }}/documentation#list-of-predefined-notification-and-commands">List of predefined notification and commands</a> section for all available notifications and commands.</span>

**Inline randomizer**

Inline randomizer will allow you to randomize a message further by substituting the block with one of its options.
```
[Hello;Hi;Hey;Hewwo;Ello]
```
<span class="icon idea">Note: Inline randomizers can be used multiple times in one message.</span>

**List of substitutes**
- `{sender}` - Message sender / Notification initiator
- `{recipient}` - Recipient (Used in gift sub and shoutout)
- `{bits}` - Number of bits
- `{sub_tier}` - sub tier (Used in sub, resub, subgift and anonsubgift. Messages: Tier 1, Tier 2, Tier 3, Prime)
- `{months}` - Number of months (cumulative, used in sub and resub)
- `{months_streak}` - Number of months in a row (used in sub and resub)
- `{activity}` - Activity (Used in shoutout for stream category)
- `{viewers}` - Number of viewers (Used in raid)

### Customize user activities
"Activities" are used for shoutout command to append customized stream category text.
Same as with "Messages", multiple reply lines and inline randomizer can be used.
Blank space at the beginning of activity text is **required**.

*Example:*
```
    "Activities": {
        "Game": [
            " and they were last playing {activity}"
        ]
    }
```

**List of substitutes**
- `{activity}` - Game name or stream category

**List of activities**
- Game
- Art
- Makers and Crafting
- Food & Drink
- Music & Performing Arts
- Beauty & Body Art
- Science & Technology
- Just Chatting
- Travel & Outdoors
- Sports & Fitness
- Tabletop RPGs
- Special Events
- Talk Shows & Podcasts
- ASMR

### Enabling/Disabling notifications and commands
You can enable or disable selective notifications and commands.
By default, all notifications and commands are enabled.

*Example:*
```
    "Enabled": {
        "new_chatter": false,
        "greet": true
    }
```
* (true/false)

<span class="icon info">See <a class="icon doc" href="{{ site.github.url }}/documentation#list-of-predefined-notification-and-commands">List of predefined notification and commands</a> section for all available notifications and commands.</span>

### Mapping mascot poses to notifications
PoseMapping allows you to map available mascot poses to notification.
All notification and commands will use DEFAULT mapping unless a mapping is created for them.
```
    "PoseMapping": {
        "DEFAULT": {
            "Image": "Wave",
            "Audio": "Wave"
        },
        "raid": {
            "Image": "Happy",
            "Audio": "Happy"
        },
        "!hello": {
            "Image": "Happy",
            "Audio": "Happy"
        }
    }
```
<span class="icon info">See <a class="icon doc" href="{{ site.github.url }}/documentation#list-of-predefined-notification-and-commands">List of predefined notification and commands</a> section for all available notifications and commands.</span>

### List of predefined notification and commands

- new_chatter
- greet
- follow
- raid
- host
- autohost
- sub
- resub
- subgift
- anonsubgift
- bits
- lurk
- shoutout
