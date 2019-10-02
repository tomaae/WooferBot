---
name: Basic configuration
anchor: basic-configuration
toc: 
 - name: Login information
   anchor: login-information
 - name: Miscellaneous parameters
   anchor: miscellaneous-parameters
 - name: Chat parser configuration
   anchor: chat-parser-configuration
---
This section explains basic configuration such as authentication and global parameters.

### Login information
Login information for your <a class="icon website" href="https://www.twitch.tv" target="_blank">twitch.tv</a> account. These parameters are **mandatory** for bot to work.
```
{
    "TwitchChannel": "",
    "TwitchOAUTH": ""
}
```
* <span class="icon settings">TwitchChannel</span> Channel name.
* <span class="icon settings">TwitchOAUTH</span> How to obtain a Twitch OAUTH: <a class="icon twitch" href="https://www.twitchapps.com/tmi/" target="_blank">www.twitchapps.com/tmi/</a>  
<br><span class="icon idea">Never share your Twitch OAUTH with anyone. If someone has seen your OAUTH, generate a new one as soon as possible.</span>

### Miscellaneous parameters
Miscellaneous configurable parameters.
```
{
    "CurrentMascot": "malamute",
    "GlobalVolume": 0.2,
    "MinBits": 0,
    "Bots": []
}
```
* <span class="icon settings">CurrentMascot</span> Name of active mascot.
* <span class="icon settings">GlobalVolume</span> Adjusts global volume.
* <span class="icon settings">MinBits</span> Minimum amount of bits to trigger a bit notification
* <span class="icon settings">Bots</span> List of bots on your channel. This parameter is used for ignoring greetings and parse specific messages.

Syntax:
```
"Bots": ["mybot1", "mybot2"]
```
<span class="icon idea">Note: Following bots are already included: nightbot, streamlabs, streamelements, stay_hydrated_bot, botisimo, wizebot</span>

### Chat parser configuration
Customize notifications which relies on a chat parser.
```
{
    "HostMessage": "is now hosting you.",
    "AutohostMessage": "is auto hosting you",
    "FollowMessage": "Thank you for the follow!"
}
```
* <span class="icon settings">FollowMessage</span> New follower notification is parsed from chat. If your chatbot replies with different text, modify the parameter as necessary.
* Modify <span class="icon settings">HostMessage</span> and <span class="icon settings">AutohostMessage</span> as necessary for different languages.
Host messages are send only to broadcaster as DM.
