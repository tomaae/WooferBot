---
name: Basic configuration
anchor: basic-configuration
toc: 
 - name: Global parameters
   anchor: global-parameters
 - name: Chat parser configuration
   anchor: chat-parser-configuration
---
This section explains basic configuration and global parameters.

### Global parameters
Miscellaneous configurable parameters.
```
{
    "CurrentMascot": "malamute",
    "GlobalVolume": 0.2,
    "MinBits": 0,
    "AutoShoutout": false,
    "AutoShoutoutTime": 10,
    "Bots": []
}
```
* <span class="icon settings">CurrentMascot</span> Set active mascot.
  * <a target="_blank" href="{{ site.github.url }}/mascots#beatrice">beatrice</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#cat-ragdoll">cat_ragdoll</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#cat-russian-blue">cat_russianblue</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#cat-siamese">cat_siamese</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#cat-tabby">cat_tabby</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#lydia">lydia</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#malamute">malamute</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#mango">mango</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#nyuko">nyuko</a>
  * <a target="_blank" href="{{ site.github.url }}/mascots#tem">tem</a>
* <span class="icon settings">GlobalVolume</span> Adjusts global volume.
* <span class="icon settings">MinBits</span> Minimum amount of bits to trigger a bit notification.
* <span class="icon settings">AutoShoutout</span> (true/false) Enable automatic shoutout after raid and host.
* <span class="icon settings">AutoShoutoutTime</span> Number of seconds between raid/host and automatic shoutout.
* <span class="icon settings">Bots</span> List of bots on your channel. This parameter is used for ignoring greetings and parse specific messages.

Syntax:
```
"Bots": ["mybot1", "mybot2"]
```
<span class="icon idea">Note: Following bots are already included: nightbot, streamlabs, streamelements, stay_hydrated_bot, botisimo, wizebot, moobot</span>

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
